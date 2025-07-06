"""
Event handlers for the notification module.

This module contains handlers for various events that trigger webhook notifications.
"""
from datetime import datetime
from typing import Dict, Any, Optional, List

from lato import TransactionContext, Event

from modules.event.events import (
    SeriesCreated, SeriesDeleted, SeriesUpdated, SeriesStatusUpdated,
    SeriesStarted, SeriesClosed, DriverJoinedEvent, DriverLeftEvent,
    EventScheduleAdded, EventScheduleRemoved, RaceResultUploaded, EventDeleted
)
from modules.notification.domain.value_objects import WebhookEventType
from modules.notification.domain.entity import WebhookLog, WebhookSubscription
from modules.notification.repository import WebhookRepository, WebhookSubscriptionRepository, WebhookLogRepository
from modules.notification.notification_module import notification_module
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
            log = WebhookLog(
                webhook_id=webhook.id,
                subscription_id=subscription.id,
                payload=payload,
                succeeded=False,
                timestamp=datetime.now()
            )
            log_repository.create(log)


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


@notification_module.handler(SeriesCreated)
def handle_series_created(
    event: SeriesCreated,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle SeriesCreated event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.SERIES_CREATED,
        payload,
        resource_type="Series",
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )


@notification_module.handler(SeriesDeleted)
def handle_series_deleted(
    event: SeriesDeleted,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle SeriesDeleted event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.SERIES_DELETED,
        payload,
        resource_type="Series",
        resource_id=event.id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )


@notification_module.handler(SeriesUpdated)
def handle_series_updated(
    event: SeriesUpdated,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle SeriesUpdated event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.SERIES_UPDATED,
        payload,
        resource_type="Series",
        resource_id=event.series_id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )


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
        WebhookEventType.EVENT_STARTED,
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
        WebhookEventType.EVENT_CLOSED,
        payload,
        resource_type="Series",
        resource_id=event.series_id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )


@notification_module.handler(DriverJoinedEvent)
def handle_driver_joined_event(
    event: DriverJoinedEvent,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle DriverJoinedEvent event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.DRIVER_JOINED,
        payload,
        resource_type="Event",
        resource_id=event.event_id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )


@notification_module.handler(DriverLeftEvent)
def handle_driver_left_event(
    event: DriverLeftEvent,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle DriverLeftEvent event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.DRIVER_LEFT,
        payload,
        resource_type="Event",
        resource_id=event.event_id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )


@notification_module.handler(EventScheduleAdded)
def handle_event_schedule_added(
    event: EventScheduleAdded,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle EventScheduleAdded event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.EVENT_OPEN,
        payload,
        resource_type="Event",
        resource_id=event.event_id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )


@notification_module.handler(RaceResultUploaded)
def handle_race_result_uploaded(
    event: RaceResultUploaded,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle RaceResultUploaded event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.RACE_RESULT_UPLOADED,
        payload,
        resource_type="Event",
        resource_id=event.event_id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )


@notification_module.handler(EventDeleted)
def handle_event_deleted(
    event: EventDeleted,
    ctx: TransactionContext,
    webhook_repository: WebhookRepository,
    webhook_subscription_repository: WebhookSubscriptionRepository,
    webhook_log_repository: WebhookLogRepository
) -> None:
    """Handle EventDeleted event."""
    payload = _event_to_payload(event)
    _create_delivery_logs(
        WebhookEventType.EVENT_CLOSED,
        payload,
        resource_type="Event",
        resource_id=event.event_id,
        webhook_repository=webhook_repository,
        subscription_repository=webhook_subscription_repository,
        log_repository=webhook_log_repository
    )
