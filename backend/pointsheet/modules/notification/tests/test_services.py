import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

import requests
from sqlalchemy.orm import Session

from modules.notification.services import WebhookLogService, WebhookSenderService, WebhookProcessorService
from modules.notification.domain.entity import WebhookLog
from modules.notification.domain.value_objects import WebhookPlatform
from pointsheet.models.notification import Webhook, WebhookSubscription, WebhookLog as WebhookLogModel


class TestWebhookLogService(unittest.TestCase):
    """
    Tests for the WebhookLogService class.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.session = MagicMock(spec=Session)
        self.logger = MagicMock()
        self.service = WebhookLogService(self.session, self.logger)

    def test_find_pending_logs(self):
        """Test finding pending webhook logs."""
        # Mock the session.execute().scalars().all() chain
        mock_logs = [MagicMock(spec=WebhookLogModel) for _ in range(3)]
        self.session.execute.return_value.scalars.return_value.all.return_value = mock_logs

        # Call the method
        result = self.service.find_pending_logs(limit=10)

        # Assert the result
        self.assertEqual(result, mock_logs)
        self.session.execute.assert_called_once()

    def test_find_failed_logs(self):
        """Test finding failed webhook logs."""
        # Mock the session.execute().scalars().all() chain
        mock_logs = [MagicMock(spec=WebhookLogModel) for _ in range(2)]
        self.session.execute.return_value.scalars.return_value.all.return_value = mock_logs

        # Call the method
        result = self.service.find_failed_logs(limit=5)

        # Assert the result
        self.assertEqual(result, mock_logs)
        self.session.execute.assert_called_once()

    def test_find_log_by_id(self):
        """Test finding a webhook log by ID."""
        # Mock the session.get() method
        mock_log = MagicMock(spec=WebhookLogModel)
        self.session.get.return_value = mock_log

        # Call the method
        result = self.service.find_log_by_id("test-id")

        # Assert the result
        self.assertEqual(result, mock_log)
        self.session.get.assert_called_once_with(WebhookLogModel, "test-id")

    def test_update_log_with_response(self):
        """Test updating a webhook log with a response."""
        # Create a mock log
        mock_log = MagicMock(spec=WebhookLogModel)

        # Call the method
        result = self.service.update_log_with_response(
            mock_log, 200, "OK", True
        )

        # Assert the log was updated correctly
        self.assertEqual(mock_log.http_status, 200)
        self.assertEqual(mock_log.response_body, "OK")
        self.assertEqual(mock_log.succeeded, True)

        # Assert the log was added to the session and committed
        self.session.add.assert_called_once_with(mock_log)
        self.session.commit.assert_called_once()

        # Assert the result
        self.assertEqual(result, mock_log)

    def test_update_log_with_error(self):
        """Test updating a webhook log with an error."""
        # Create a mock log
        mock_log = MagicMock(spec=WebhookLogModel)

        # Create a test error
        test_error = Exception("Test error")

        # Call the method
        result = self.service.update_log_with_error(mock_log, test_error)

        # Assert the log was updated correctly
        self.assertEqual(mock_log.http_status, 0)
        self.assertEqual(mock_log.response_body, "Test error")
        self.assertEqual(mock_log.succeeded, False)

        # Assert the log was added to the session and committed
        self.session.add.assert_called_once_with(mock_log)
        self.session.commit.assert_called_once()

        # Assert the result
        self.assertEqual(result, mock_log)


class TestWebhookSenderService(unittest.TestCase):
    """
    Tests for the WebhookSenderService class.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.logger = MagicMock()
        self.service = WebhookSenderService(self.logger)

    @patch("requests.post")
    def test_send_webhook_basic(self, mock_post):
        """Test sending a basic webhook."""
        # Create a mock webhook and response
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.target_url = "https://example.com/webhook"
        mock_webhook.platform = WebhookPlatform.GENERIC_HTTP.value
        mock_webhook.secret = None
        mock_webhook.config = None

        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Call the method
        result = self.service.send_webhook(mock_webhook, {"test": "payload"})

        # Assert the request was made correctly
        mock_post.assert_called_once_with(
            "https://example.com/webhook",
            json={"test": "payload"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        # Assert the result
        self.assertEqual(result, mock_response)

    @patch("requests.post")
    def test_send_webhook_with_secret(self, mock_post):
        """Test sending a webhook with a secret."""
        # Create a mock webhook and response
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.target_url = "https://example.com/webhook"
        mock_webhook.platform = WebhookPlatform.GENERIC_HTTP.value
        mock_webhook.secret = "test-secret"
        mock_webhook.config = None

        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Call the method
        result = self.service.send_webhook(mock_webhook, {"test": "payload"})

        # Assert the request was made correctly
        mock_post.assert_called_once_with(
            "https://example.com/webhook",
            json={"test": "payload"},
            headers={
                "Content-Type": "application/json",
                "Authorization": "test-secret"
            },
            timeout=10
        )

        # Assert the result
        self.assertEqual(result, mock_response)

    @patch("requests.post")
    def test_send_webhook_with_custom_headers(self, mock_post):
        """Test sending a webhook with custom headers."""
        # Create a mock webhook and response
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.target_url = "https://example.com/webhook"
        mock_webhook.platform = WebhookPlatform.GENERIC_HTTP.value
        mock_webhook.secret = None
        mock_webhook.config = {"headers": {"X-Custom-Header": "test-value"}}

        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Call the method
        result = self.service.send_webhook(mock_webhook, {"test": "payload"})

        # Assert the request was made correctly
        mock_post.assert_called_once_with(
            "https://example.com/webhook",
            json={"test": "payload"},
            headers={
                "Content-Type": "application/json",
                "X-Custom-Header": "test-value"
            },
            timeout=10
        )

        # Assert the result
        self.assertEqual(result, mock_response)


class TestWebhookProcessorService(unittest.TestCase):
    """
    Tests for the WebhookProcessorService class.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.session = MagicMock(spec=Session)
        self.logger = MagicMock()
        self.log_service = MagicMock(spec=WebhookLogService)
        self.sender_service = MagicMock(spec=WebhookSenderService)
        self.service = WebhookProcessorService(
            self.log_service, self.sender_service, self.session, self.logger
        )

    def test_process_pending_webhooks_no_logs(self):
        """Test processing pending webhooks when there are none."""
        # Mock the log service to return no logs
        self.log_service.find_pending_logs.return_value = []

        # Call the method
        success_count, failure_count = self.service.process_pending_webhooks()

        # Assert the result
        self.assertEqual(success_count, 0)
        self.assertEqual(failure_count, 0)
        self.log_service.find_pending_logs.assert_called_once_with(50)
        self.sender_service.send_webhook.assert_not_called()

    def test_process_pending_webhooks_dry_run(self):
        """Test processing pending webhooks in dry run mode."""
        # Create mock logs and webhooks
        mock_log = MagicMock(spec=WebhookLogModel)
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.enabled = True

        # Mock the log service
        self.log_service.find_pending_logs.return_value = [mock_log]
        self.log_service.get_webhook_for_log.return_value = mock_webhook

        # Call the method with dry_run=True
        success_count, failure_count = self.service.process_pending_webhooks(dry_run=True)

        # Assert the result
        self.assertEqual(success_count, 0)
        self.assertEqual(failure_count, 0)
        self.log_service.find_pending_logs.assert_called_once_with(50)
        self.sender_service.send_webhook.assert_not_called()

    def test_process_pending_webhooks_success(self):
        """Test processing pending webhooks with a successful response."""
        # Create mock logs, webhooks, and responses
        mock_log = MagicMock(spec=WebhookLogModel)
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.enabled = True
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "OK"

        # Mock the log service and sender service
        self.log_service.find_pending_logs.return_value = [mock_log]
        self.log_service.get_webhook_for_log.return_value = mock_webhook
        self.sender_service.send_webhook.return_value = mock_response

        # Call the method
        success_count, failure_count = self.service.process_pending_webhooks()

        # Assert the result
        self.assertEqual(success_count, 1)
        self.assertEqual(failure_count, 0)
        self.log_service.find_pending_logs.assert_called_once_with(50)
        self.sender_service.send_webhook.assert_called_once()
        self.log_service.update_log_with_response.assert_called_once_with(
            mock_log, 200, "OK", True
        )

    def test_process_pending_webhooks_failure(self):
        """Test processing pending webhooks with a failed response."""
        # Create mock logs, webhooks, and responses
        mock_log = MagicMock(spec=WebhookLogModel)
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.enabled = True
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        # Mock the log service and sender service
        self.log_service.find_pending_logs.return_value = [mock_log]
        self.log_service.get_webhook_for_log.return_value = mock_webhook
        self.sender_service.send_webhook.return_value = mock_response

        # Call the method
        success_count, failure_count = self.service.process_pending_webhooks()

        # Assert the result
        self.assertEqual(success_count, 0)
        self.assertEqual(failure_count, 1)
        self.log_service.find_pending_logs.assert_called_once_with(50)
        self.sender_service.send_webhook.assert_called_once()
        self.log_service.update_log_with_response.assert_called_once_with(
            mock_log, 404, "Not Found", False
        )

    def test_process_pending_webhooks_exception(self):
        """Test processing pending webhooks with an exception."""
        # Create mock logs and webhooks
        mock_log = MagicMock(spec=WebhookLogModel)
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.enabled = True

        # Mock the log service and sender service
        self.log_service.find_pending_logs.return_value = [mock_log]
        self.log_service.get_webhook_for_log.return_value = mock_webhook
        self.sender_service.send_webhook.side_effect = Exception("Test error")

        # Call the method
        success_count, failure_count = self.service.process_pending_webhooks()

        # Assert the result
        self.assertEqual(success_count, 0)
        self.assertEqual(failure_count, 1)
        self.log_service.find_pending_logs.assert_called_once_with(50)
        self.sender_service.send_webhook.assert_called_once()
        self.log_service.update_log_with_error.assert_called_once()

    def test_retry_webhook_success(self):
        """Test retrying a webhook with a successful response."""
        # Create mock logs, webhooks, and responses
        mock_log = MagicMock(spec=WebhookLogModel)
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.enabled = True
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "OK"

        # Mock the log service and sender service
        self.log_service.find_log_by_id.return_value = mock_log
        self.log_service.get_webhook_for_log.return_value = mock_webhook
        self.sender_service.send_webhook.return_value = mock_response

        # Call the method
        result = self.service.retry_webhook("test-id")

        # Assert the result
        self.assertTrue(result)
        self.log_service.find_log_by_id.assert_called_once_with("test-id")
        self.sender_service.send_webhook.assert_called_once()
        self.log_service.update_log_with_response.assert_called_once_with(
            mock_log, 200, "OK", True
        )

    def test_retry_webhook_failure(self):
        """Test retrying a webhook with a failed response."""
        # Create mock logs, webhooks, and responses
        mock_log = MagicMock(spec=WebhookLogModel)
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.enabled = True
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        # Mock the log service and sender service
        self.log_service.find_log_by_id.return_value = mock_log
        self.log_service.get_webhook_for_log.return_value = mock_webhook
        self.sender_service.send_webhook.return_value = mock_response

        # Call the method
        result = self.service.retry_webhook("test-id")

        # Assert the result
        self.assertFalse(result)
        self.log_service.find_log_by_id.assert_called_once_with("test-id")
        self.sender_service.send_webhook.assert_called_once()
        self.log_service.update_log_with_response.assert_called_once_with(
            mock_log, 404, "Not Found", False
        )


if __name__ == "__main__":
    unittest.main()
