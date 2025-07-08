"""
Event handlers for the notification module.

This module contains handlers for various events that trigger webhook notifications.
"""
from datetime import datetime
from typing import Dict, Any, Optional

from lato import TransactionContext, Event

from modules.event.events import (
    SeriesStarted, SeriesClosed
)
from modules.notification.domain.value_objects import WebhookEventType
from modules.notification.domain.entity import WebhookLog
from modules.notification.repository import WebhookRepository, WebhookSubscriptionRepository, WebhookLogRepository
from modules.notification.notification_module import notification_module
from modules.notification.formatters import DynamicWebhookFormatterFactory
from pointsheet.domain.types import EntityId


def _create_delivery_logs(
    event_type: WebhookEventType,
    payload: Dict[str, Any],
    resource_type: Optional[str] = None,
    resource_id: Optional[EntityId] = None,
    webhook_repository: WebhookRepository = None,
    subscription_repository: WebhookSubscriptionRepository = None,
    log_repository: WebhookLogRepository = None
) -> None:
    """
    Create webhook delivery logs for a specific event type.

    First tries to find subscriptions specific to the resource,
    then falls back to general subscriptions for the event type,
    and finally to default subscriptions if none are found.

    Args:
        event_type: The type of event
        payload: The event payload
        resource_type: Optional resource type (e.g., "Event", "Series")
        resource_id: Optional resource ID
        webhook_repository: Repository for webhooks
        subscription_repository: Repository for webhook subscriptions
        log_repository: Repository for webhook logs
    """
    # Find subscriptions in order of specificity
    subscriptions = subscription_repository.find_by_event_type(
        event_type, resource_type, resource_id
    )

    # If no specific subscriptions found, use defaults
    if not subscriptions:
        subscriptions = subscription_repository.find_default_subscriptions()

    # Create logs for each subscription
    for subscription in subscriptions:
        webhook = webhook_repository.find_by_id(subscription.webhook_id)
        if webhook and webhook.enabled:
            try:
                # Get event type from payload
                event_type_name = payload.get("event_type", "Unknown")

                # Format the payload for the specific platform and event type
                formatter = DynamicWebhookFormatterFactory.create_formatter(webhook.platform, event_type_name)
                formatted_payload = formatter.format_payload(webhook, payload)

                # Create the webhook log with the formatted payload
                log = WebhookLog(
                    webhook_id=webhook.id,
                    subscription_id=subscription.id,
                    payload=formatted_payload,
                    succeeded=False,
                    timestamp=datetime.now()
                )
                log_repository.add(log)
            except ValueError as e:
                # Log error if platform is not supported
                print(f"Error formatting webhook payload: {str(e)}")


def _event_to_payload(event: Event) -> Dict[str, Any]:
    """
    Convert an event to a payload dictionary.

    Args:
        event: The event to convert

    Returns:
        A dictionary containing the event data
    """
    # Convert event to dictionary
    event_dict = event.model_dump()

    # Add event type
    event_dict["event_type"] = event.__class__.__name__

    return event_dict


@notification_module.handler(SeriesStarted)
def handle_series_started(
    event: SeriesStarted,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle SeriesStarted event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.SERIES_STARTED,
        payload,
        resource_type="Series",
        resource_id=event.series_id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )


@notification_module.handler(SeriesClosed)
def handle_series_closed(
    event: SeriesClosed,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle SeriesClosed event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.SERIES_CLOSED,
        payload,
        resource_type="Series",
        resource_id=event.series_id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )
