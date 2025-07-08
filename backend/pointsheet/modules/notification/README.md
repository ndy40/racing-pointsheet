# Webhook Notification Module

This module provides webhook notification functionality for the Racing Pointsheet application. It allows the application to send webhook notifications to configured endpoints like Discord, Slack, Telegram, etc.

## Architecture

The webhook notification module follows a service-oriented architecture with the following components:

### Domain Models

- `Webhook`: Represents a webhook configuration, including the target URL, platform, and authentication details.
- `WebhookSubscription`: Defines which events a webhook should be triggered for, optionally filtered by resource type and ID.
- `WebhookLog`: Tracks the delivery of webhooks, including the webhook, subscription, payload, response, and status.

### Value Objects

- `WebhookPlatform`: Enum representing different webhook platforms (Discord, Slack, Telegram, Generic HTTP).
- `WebhookEventType`: Enum representing different event types that can trigger notifications.
- `WebhookDeliveryStatus`: Enum representing the status of a webhook delivery (pending, delivered, failed).

### Services

The module uses a service-oriented architecture to separate concerns and make the code more testable:

- `WebhookLogService`: Manages webhook logs, including finding, listing, and updating logs.
- `WebhookSenderService`: Handles sending webhooks to their destinations, including formatting payloads and handling authentication.
- `WebhookProcessorService`: Orchestrates the webhook processing workflow, including finding pending webhooks, sending them, and updating their status.

### CLI Commands

The module provides CLI commands for managing webhook notifications:

- `webhook process`: Process pending webhook notifications.
- `webhook list`: List webhook logs with various filters.
- `webhook retry`: Retry failed webhook deliveries.

## Usage

### Processing Webhooks

To process pending webhook notifications:

```bash
python -m pointsheet.main webhook process
```

Options:
- `--limit INTEGER`: Maximum number of webhooks to process (default: 50)
- `--timeout INTEGER`: HTTP request timeout in seconds (default: 10)
- `--dry-run`: Don't actually send webhooks, just log what would be sent

### Listing Webhook Logs

To list webhook logs:

```bash
python -m pointsheet.main webhook list
```

Options:
- `--limit INTEGER`: Maximum number of logs to show (default: 20)
- `--succeeded BOOLEAN`: Filter by success status (True/False)
- `--webhook-id TEXT`: Filter by webhook ID
- `--days INTEGER`: Show logs from the last N days (default: 1)

### Retrying Failed Webhooks

To retry failed webhook deliveries:

```bash
python -m pointsheet.main webhook retry --all
```

Options:
- `--id TEXT`: Retry a specific webhook log by ID
- `--all`: Retry all failed webhooks
- `--limit INTEGER`: Maximum number of webhooks to retry (default: 10)
- `--timeout INTEGER`: HTTP request timeout in seconds (default: 10)

## Lock Mechanism

The webhook CLI includes a lock mechanism to ensure that only one instance can run at a time. This is important when running the CLI as a cron job to prevent multiple instances from processing the same webhooks simultaneously.

### How It Works

1. When a CLI command is executed, it attempts to acquire a lock by creating a lock file at `/tmp/webhook_cli.lock`.
2. If the lock file already exists, the CLI checks if the process ID in the file is still running:
   - If the process is still running, the CLI exits with a message.
   - If the process is not running (stale lock), the CLI removes the lock file and creates a new one.
3. When the CLI command finishes executing, it releases the lock by removing the lock file.
4. The lock is also released if the CLI crashes or is terminated unexpectedly, thanks to the `atexit` module.

### Benefits

- Prevents duplicate webhook deliveries by ensuring only one instance of the CLI runs at a time.
- Automatically handles stale locks from crashed or terminated processes.
- Provides clear logging about lock acquisition and release.
- Ensures the lock is always released, even if an exception occurs.

## Testing

The module includes comprehensive unit tests for the service classes. To run the tests:

```bash
python -m unittest modules.notification.tests.test_services
```

## Benefits of the Service-Oriented Architecture

The service-oriented architecture provides several benefits:

1. **Separation of Concerns**: Each service has a single responsibility, making the code easier to understand and maintain.
2. **Testability**: The services can be tested in isolation, making it easier to write comprehensive unit tests.
3. **Reusability**: The services can be used in different contexts, not just the CLI commands.
4. **Flexibility**: The services can be extended or modified without affecting other parts of the system.
5. **Logging**: Each service has its own logger, making it easier to track what's happening in the system.
