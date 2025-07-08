import os
import sys
import logging
import atexit
from typing import Optional

import click
import requests

from modules.notification.services import WebhookLogService, WebhookSenderService, WebhookProcessorService

# Define lock file path
LOCK_FILE = "/tmp/webhook_cli.lock"

def acquire_lock():
    """
    Acquire a lock to ensure only one instance of the CLI can run at a time.

    If another instance is already running, exit with a message.
    """
    # Check if lock file exists
    if os.path.exists(LOCK_FILE):
        # Read the PID from the lock file
        try:
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())

            # Check if the process is still running
            try:
                # Sending signal 0 to a process will raise an OSError if the process is not running
                os.kill(pid, 0)
                logger.warning(f"Another instance of webhook_cli is already running (PID: {pid}). Exiting.")
                sys.exit(1)
            except OSError:
                # Process is not running, we can acquire the lock
                logger.info(f"Stale lock file found. Previous process (PID: {pid}) is not running.")
        except (ValueError, IOError) as e:
            # Invalid PID or error reading the file
            logger.warning(f"Invalid lock file found: {str(e)}. Removing it.")

    # Create lock file with current PID
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

    logger.info(f"Lock acquired (PID: {os.getpid()}).")

    # Register function to release lock on exit
    atexit.register(release_lock)

def release_lock():
    """
    Release the lock by removing the lock file.
    """
    if os.path.exists(LOCK_FILE):
        try:
            # Check if the lock file contains our PID
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())

            if pid == os.getpid():
                os.remove(LOCK_FILE)
                logger.info(f"Lock released (PID: {os.getpid()}).")
            else:
                logger.warning(f"Lock file contains different PID: {pid}, not removing.")
        except (ValueError, IOError) as e:
            logger.warning(f"Error reading lock file: {str(e)}. Removing it anyway.")
            try:
                os.remove(LOCK_FILE)
            except OSError as e:
                logger.warning(f"Error removing lock file: {str(e)}")

# Set up logging
logger = logging.getLogger("webhook_cli")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

@click.group(name="webhook")
def webhook_cli():
    """Commands for managing webhook notifications."""
    pass

@webhook_cli.command(name="process", help="Process pending webhook notifications")
@click.option("--limit", default=50, help="Maximum number of webhooks to process")
@click.option("--timeout", default=10, help="HTTP request timeout in seconds")
@click.option("--dry-run", is_flag=True, help="Don't actually send webhooks, just log what would be sent")
def process_webhooks(limit: int, timeout: int, dry_run: bool):
    """Process pending webhook notifications."""
    # Acquire lock to ensure only one instance is running
    acquire_lock()

    processor = WebhookProcessorService(logger=logger)

    try:
        success_count, failure_count = processor.process_pending_webhooks(limit, timeout, dry_run)

        if success_count > 0 or failure_count > 0:
            logger.info(f"Processed {success_count + failure_count} webhooks: {success_count} succeeded, {failure_count} failed")

    except ConnectionError as e:
        logger.error(f"Connection error while processing webhooks: {str(e)}")
    except TimeoutError as e:
        logger.error(f"Timeout error while processing webhooks: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing webhooks: {str(e)}")
    finally:
        # Always close the session to avoid resource leaks
        if hasattr(processor, 'session'):
            processor.session.close()

        # Release the lock
        release_lock()

@webhook_cli.command(name="list", help="List webhook logs")
@click.option("--limit", default=20, help="Maximum number of logs to show")
@click.option("--succeeded", type=bool, help="Filter by success status")
@click.option("--webhook-id", help="Filter by webhook ID")
@click.option("--days", default=1, help="Show logs from the last N days")
def list_webhook_logs(limit: int, succeeded: Optional[bool], webhook_id: Optional[str], days: int):
    """List webhook logs."""
    # Acquire lock to ensure only one instance is running
    acquire_lock()

    log_service = WebhookLogService(logger=logger)

    try:
        logs = log_service.list_logs(limit, succeeded, webhook_id, days)

        if not logs:
            click.echo("No webhook logs found.")
            return

        # Print the logs
        click.echo(f"Found {len(logs)} webhook logs:")
        for log in logs:
            status = "✅" if log.succeeded else "❌"
            timestamp = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            http_status = log.http_status or "N/A"
            click.echo(f"{status} [{timestamp}] ID: {log.id} HTTP: {http_status}")

    except Exception as e:
        click.echo(f"Error listing webhook logs: {str(e)}")
    finally:
        # Always close the session to avoid resource leaks
        if hasattr(log_service, 'session'):
            log_service.session.close()

        # Release the lock
        release_lock()

@webhook_cli.command(name="retry", help="Retry failed webhook deliveries")
@click.option("--id", help="Retry a specific webhook log by ID")
@click.option("--all", "retry_all", is_flag=True, help="Retry all failed webhooks")
@click.option("--limit", default=10, help="Maximum number of webhooks to retry")
@click.option("--timeout", default=10, help="HTTP request timeout in seconds")
def retry_webhooks(id: Optional[str], retry_all: bool, limit: int, timeout: int):
    """Retry failed webhook deliveries."""
    # Acquire lock to ensure only one instance is running
    acquire_lock()

    if not id and not retry_all:
        click.echo("Please specify either --id or --all")
        release_lock()  # Release lock before returning
        return

    processor = WebhookProcessorService(logger=logger)

    try:
        if id:
            # Retry a specific webhook log
            result = processor.retry_webhook(id, timeout)
            if result:
                click.echo(f"Webhook {id} retry succeeded")
            else:
                click.echo(f"Webhook {id} retry failed")
        else:
            # Retry all failed webhook logs
            success_count, failure_count = processor.retry_failed_webhooks(limit, timeout)

            if success_count > 0 or failure_count > 0:
                click.echo(f"Retried {success_count + failure_count} webhooks: {success_count} succeeded, {failure_count} failed")
            else:
                click.echo("No failed webhook logs to retry.")

    except ConnectionError as e:
        click.echo(f"Connection error while retrying webhooks: {str(e)}")
    except TimeoutError as e:
        click.echo(f"Timeout error while retrying webhooks: {str(e)}")
    except Exception as e:
        click.echo(f"Error retrying webhooks: {str(e)}")
    finally:
        # Always close the session to avoid resource leaks
        if hasattr(processor, 'session'):
            processor.session.close()

        # Release the lock
        release_lock()


if __name__ == "__main__":
    webhook_cli()
