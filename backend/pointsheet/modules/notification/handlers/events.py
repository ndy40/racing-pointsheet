from lato import TransactionContext

from modules.notification.notification_module import notification_module
from modules.notification.repository import WebhookRepository, WebhookSubscriptionRepository, WebhookLogRepository
from modules.event.events import DriverJoinedEvent, DriverLeftEvent, EventScheduleAdded, RaceResultUploaded, \
    EventDeleted
from modules.notification import WebhookEventType
from modules.notification.handlers.series import _event_to_payload, _create_delivery_logs


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
