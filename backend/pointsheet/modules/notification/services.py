import logging
import sys
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple

import requests
from sqlalchemy import select
from sqlalchemy.orm import Session

from pointsheet.db import get_session
from modules.notification.domain.entity import WebhookLog
from modules.notification.domain.value_objects import WebhookPlatform
from modules.notification.formatters import WebhookFormatterFactory
from pointsheet.models.notification import Webhook, WebhookSubscription, WebhookLog as WebhookLogModel


class WebhookLogService:
    """
    Service for managing webhook logs.
    
    This service provides methods for finding, listing, and updating webhook logs.
    """
    
    def __init__(self, session: Optional[Session] = None, logger: Optional[logging.Logger] = None):
        """
        Initialize the webhook log service.
        
        Args:
            session: The database session to use
            logger: The logger to use
        """
        self.session = session or next(get_session())
        self.logger = logger or logging.getLogger(__name__)
    
    def find_pending_logs(self, limit: int = 50) -> List[WebhookLogModel]:
        """
        Find pending webhook logs.
        
        Args:
            limit: Maximum number of logs to return
            
        Returns:
            A list of pending webhook logs
        """
        stmt = select(WebhookLogModel).where(
            WebhookLogModel.succeeded == False,
            WebhookLogModel.http_status.is_(None)
        ).limit(limit)
        
        return self.session.execute(stmt).scalars().all()
    
    def find_failed_logs(self, limit: int = 10) -> List[WebhookLogModel]:
        """
        Find failed webhook logs.
        
        Args:
            limit: Maximum number of logs to return
            
        Returns:
            A list of failed webhook logs
        """
        stmt = select(WebhookLogModel).where(
            WebhookLogModel.succeeded == False,
            WebhookLogModel.http_status.isnot(None)  # Only logs that have been attempted
        ).limit(limit)
        
        return self.session.execute(stmt).scalars().all()
    
    def find_log_by_id(self, log_id: str) -> Optional[WebhookLogModel]:
        """
        Find a webhook log by ID.
        
        Args:
            log_id: The ID of the log to find
            
        Returns:
            The webhook log, or None if not found
        """
        return self.session.get(WebhookLogModel, log_id)
    
    def list_logs(
        self, 
        limit: int = 20, 
        succeeded: Optional[bool] = None, 
        webhook_id: Optional[str] = None, 
        days: int = 1
    ) -> List[WebhookLogModel]:
        """
        List webhook logs with filters.
        
        Args:
            limit: Maximum number of logs to return
            succeeded: Filter by success status
            webhook_id: Filter by webhook ID
            days: Show logs from the last N days
            
        Returns:
            A list of webhook logs
        """
        stmt = select(WebhookLogModel).order_by(WebhookLogModel.timestamp.desc())
        
        if succeeded is not None:
            stmt = stmt.where(WebhookLogModel.succeeded == succeeded)
        
        if webhook_id:
            stmt = stmt.where(WebhookLogModel.webhook_id == webhook_id)
        
        if days:
            cutoff = datetime.now() - timedelta(days=days)
            stmt = stmt.where(WebhookLogModel.timestamp >= cutoff)
        
        stmt = stmt.limit(limit)
        
        return self.session.execute(stmt).scalars().all()
    
    def update_log_with_response(
        self, 
        log: WebhookLogModel, 
        status_code: int, 
        response_body: str, 
        succeeded: bool
    ) -> WebhookLogModel:
        """
        Update a webhook log with a response.
        
        Args:
            log: The webhook log to update
            status_code: The HTTP status code
            response_body: The response body
            succeeded: Whether the webhook was delivered successfully
            
        Returns:
            The updated webhook log
        """
        log.http_status = status_code
        log.response_body = response_body[:1000]  # Limit response body size
        log.succeeded = succeeded
        
        self.session.add(log)
        self.session.commit()
        
        return log
    
    def update_log_with_error(self, log: WebhookLogModel, error: Exception) -> WebhookLogModel:
        """
        Update a webhook log with an error.
        
        Args:
            log: The webhook log to update
            error: The error that occurred
            
        Returns:
            The updated webhook log
        """
        log.http_status = 0
        log.response_body = str(error)
        log.succeeded = False
        
        self.session.add(log)
        self.session.commit()
        
        return log
    
    def get_webhook_for_log(self, log: WebhookLogModel) -> Optional[Webhook]:
        """
        Get the webhook configuration for a log.
        
        Args:
            log: The webhook log
            
        Returns:
            The webhook configuration, or None if not found
        """
        return self.session.get(Webhook, log.webhook_id)
    
    def get_subscription_for_log(self, log: WebhookLogModel) -> Optional[WebhookSubscription]:
        """
        Get the webhook subscription for a log.
        
        Args:
            log: The webhook log
            
        Returns:
            The webhook subscription, or None if not found or not set
        """
        if not log.subscription_id:
            return None
        
        return self.session.get(WebhookSubscription, log.subscription_id)


class WebhookSenderService:
    """
    Service for sending webhooks.
    
    This service provides methods for sending webhooks to their destinations.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the webhook sender service.
        
        Args:
            logger: The logger to use
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def send_webhook(self, webhook: Webhook, payload: Dict[str, Any], timeout: int = 10) -> requests.Response:
        """
        Send a webhook notification.
        
        Args:
            webhook: The webhook configuration
            payload: The payload to send
            timeout: The HTTP request timeout in seconds
            
        Returns:
            The HTTP response
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add custom headers if specified
        if webhook.config and "headers" in webhook.config:
            headers.update(webhook.config["headers"])
        
        # Add authorization header if secret is specified
        if webhook.secret:
            if webhook.platform == WebhookPlatform.DISCORD.value:
                # Discord uses the secret directly in the URL
                pass
            elif webhook.platform == WebhookPlatform.SLACK.value:
                # Slack uses Bearer token auth
                headers["Authorization"] = f"Bearer {webhook.secret}"
            else:
                # Generic auth
                headers["Authorization"] = webhook.secret
        
        # Send the request
        self.logger.debug(f"Sending webhook to {webhook.target_url}")
        response = requests.post(
            webhook.target_url,
            json=payload,
            headers=headers,
            timeout=timeout
        )
        self.logger.debug(f"Received response with status code {response.status_code}")
        
        return response


class WebhookProcessorService:
    """
    Service for processing webhooks.
    
    This service provides methods for processing pending webhooks and retrying failed webhooks.
    """
    
    def __init__(
        self, 
        log_service: Optional[WebhookLogService] = None,
        sender_service: Optional[WebhookSenderService] = None,
        session: Optional[Session] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the webhook processor service.
        
        Args:
            log_service: The webhook log service to use
            sender_service: The webhook sender service to use
            session: The database session to use
            logger: The logger to use
        """
        self.session = session or next(get_session())
        self.logger = logger or logging.getLogger(__name__)
        self.log_service = log_service or WebhookLogService(self.session, self.logger)
        self.sender_service = sender_service or WebhookSenderService(self.logger)
    
    def process_pending_webhooks(self, limit: int = 50, timeout: int = 10, dry_run: bool = False) -> Tuple[int, int]:
        """
        Process pending webhook notifications.
        
        Args:
            limit: Maximum number of webhooks to process
            timeout: HTTP request timeout in seconds
            dry_run: Don't actually send webhooks, just log what would be sent
            
        Returns:
            A tuple of (success_count, failure_count)
        """
        success_count = 0
        failure_count = 0
        
        try:
            # Find pending webhook logs
            pending_logs = self.log_service.find_pending_logs(limit)
            
            if not pending_logs:
                self.logger.info("No pending webhook notifications found.")
                return success_count, failure_count
            
            self.logger.info(f"Found {len(pending_logs)} pending webhook notifications.")
            
            for log_model in pending_logs:
                # Get the webhook configuration
                webhook = self.log_service.get_webhook_for_log(log_model)
                if not webhook:
                    self.logger.warning(f"Webhook {log_model.webhook_id} not found for log {log_model.id}")
                    continue
                
                if not webhook.enabled:
                    self.logger.info(f"Skipping disabled webhook {webhook.id}")
                    continue
                
                # Get the subscription if available
                subscription = self.log_service.get_subscription_for_log(log_model)
                
                # Log what we're about to do
                self.logger.info(f"Processing webhook log {log_model.id} for webhook {webhook.id} ({webhook.platform})")
                
                if dry_run:
                    self.logger.info(f"DRY RUN: Would send to {webhook.target_url}")
                    continue
                
                try:
                    # Send the webhook
                    response = self.sender_service.send_webhook(webhook, log_model.payload, timeout)
                    
                    # Update the log with the response
                    succeeded = 200 <= response.status_code < 300
                    self.log_service.update_log_with_response(
                        log_model, 
                        response.status_code, 
                        response.text, 
                        succeeded
                    )
                    
                    if succeeded:
                        success_count += 1
                        self.logger.info(f"Webhook {log_model.id} sent with status {response.status_code}")
                    else:
                        failure_count += 1
                        self.logger.warning(f"Webhook {log_model.id} failed with status {response.status_code}")
                except Exception as e:
                    # Log the error and update the log
                    failure_count += 1
                    self.logger.error(f"Error sending webhook {log_model.id}: {str(e)}")
                    self.log_service.update_log_with_error(log_model, e)
        
        except Exception as e:
            self.logger.error(f"Error processing webhooks: {str(e)}")
            self.session.rollback()
        
        return success_count, failure_count
    
    def retry_webhook(self, log_id: str, timeout: int = 10) -> bool:
        """
        Retry a specific webhook delivery.
        
        Args:
            log_id: The ID of the webhook log to retry
            timeout: HTTP request timeout in seconds
            
        Returns:
            True if the webhook was sent successfully, False otherwise
        """
        try:
            # Find the webhook log
            log_model = self.log_service.find_log_by_id(log_id)
            if not log_model:
                self.logger.warning(f"Webhook log {log_id} not found.")
                return False
            
            # Get the webhook configuration
            webhook = self.log_service.get_webhook_for_log(log_model)
            if not webhook:
                self.logger.warning(f"Webhook {log_model.webhook_id} not found for log {log_model.id}")
                return False
            
            if not webhook.enabled:
                self.logger.info(f"Skipping disabled webhook {webhook.id}")
                return False
            
            self.logger.info(f"Retrying webhook log {log_model.id}...")
            
            try:
                # Send the webhook
                response = self.sender_service.send_webhook(webhook, log_model.payload, timeout)
                
                # Update the log with the response
                succeeded = 200 <= response.status_code < 300
                self.log_service.update_log_with_response(
                    log_model, 
                    response.status_code, 
                    response.text, 
                    succeeded
                )
                
                status = "succeeded" if succeeded else "failed"
                self.logger.info(f"Webhook {log_model.id} retry {status} with status {response.status_code}")
                
                return succeeded
            except Exception as e:
                # Log the error and update the log
                self.logger.error(f"Error retrying webhook {log_model.id}: {str(e)}")
                self.log_service.update_log_with_error(log_model, e)
                return False
        
        except Exception as e:
            self.logger.error(f"Error retrying webhook: {str(e)}")
            self.session.rollback()
            return False
    
    def retry_failed_webhooks(self, limit: int = 10, timeout: int = 10) -> Tuple[int, int]:
        """
        Retry failed webhook deliveries.
        
        Args:
            limit: Maximum number of webhooks to retry
            timeout: HTTP request timeout in seconds
            
        Returns:
            A tuple of (success_count, failure_count)
        """
        success_count = 0
        failure_count = 0
        
        try:
            # Find failed webhook logs
            logs_to_retry = self.log_service.find_failed_logs(limit)
            
            if not logs_to_retry:
                self.logger.info("No failed webhook logs to retry.")
                return success_count, failure_count
            
            self.logger.info(f"Retrying {len(logs_to_retry)} webhook logs...")
            
            for log_model in logs_to_retry:
                if self.retry_webhook(log_model.id, timeout):
                    success_count += 1
                else:
                    failure_count += 1
        
        except Exception as e:
            self.logger.error(f"Error retrying webhooks: {str(e)}")
            self.session.rollback()
        
        return success_count, failure_count