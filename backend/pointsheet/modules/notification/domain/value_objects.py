from enum import Enum


class WebhookPlatform(str, Enum):
    """
    Enum representing different webhook platforms.
    """
    DISCORD = "discord"
    SLACK = "slack"
    TELEGRAM = "telegram"
    GENERIC_HTTP = "generic_http"


class WebhookEventType(str, Enum):
    """
    Enum representing different event types that can trigger notifications.
    """
    # Series events
    SERIES_CREATED = "series.created"
    SERIES_UPDATED = "series.updated"
    SERIES_DELETED = "series.deleted"
    SERIES_STARTED = "series.started"
    SERIES_CLOSED = "series.closed"

    # Event model events
    EVENT_OPEN = "event.open"
    EVENT_COMPLETED = "event.completed"
    EVENT_CLOSED = "event.closed"
    EVENT_STARTED = "event.started"
    RACE_RESULT_UPLOADED = "event.result_uploaded"

    # Driver events
    DRIVER_JOINED = "event.driver.joined"
    DRIVER_LEFT = "event.driver.left"


class WebhookDeliveryStatus(str, Enum):
    """
    Enum representing the status of a webhook delivery.
    """
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
