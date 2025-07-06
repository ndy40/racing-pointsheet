"""
Notification module for sending webhook notifications to configured endpoints.

This module contains models and event handlers for sending webhook notifications
to configured endpoints like Discord, Slack, Telegram, etc. It also tracks
delivered webhooks with a WebhookLog.
"""

from modules.notification.domain.entity import Webhook, WebhookSubscription, WebhookLog
from modules.notification.domain.value_objects import WebhookPlatform, WebhookEventType, WebhookDeliveryStatus
from modules.notification.repository import WebhookRepository, WebhookSubscriptionRepository, WebhookLogRepository
from modules.notification.notification_module import notification_module
import modules.notification.handlers


__all__ = [
    "Webhook",
    "WebhookSubscription",
    "WebhookLog",
    "WebhookPlatform",
    "WebhookEventType",
    "WebhookDeliveryStatus",
    "WebhookRepository",
    "WebhookSubscriptionRepository",
    "WebhookLogRepository",
    "notification_module",
]
