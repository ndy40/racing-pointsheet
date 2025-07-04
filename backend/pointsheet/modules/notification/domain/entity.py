from datetime import datetime
from typing import Dict, Optional, List, Any

from pydantic import BaseModel, Field

from pointsheet.domain.entity import AggregateRoot
from pointsheet.domain.types import EntityId, uuid_default
from modules.notification.domain.value_objects import WebhookPlatform, WebhookEventType, WebhookDeliveryStatus


class Webhook(AggregateRoot):
    """
    Entity representing a webhook configuration.

    This entity stores the configuration for a webhook endpoint, including the URL,
    platform type, and optional configuration details.
    """
    name: Optional[str] = None
    target_url: str
    platform: WebhookPlatform
    secret: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


class WebhookSubscription(AggregateRoot):
    """
    Entity representing a webhook subscription.

    This entity defines which events a webhook should be triggered for,
    optionally filtered by resource type and ID.
    """
    webhook_id: EntityId
    event_type: WebhookEventType
    resource_type: Optional[str] = None
    resource_id: Optional[EntityId] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


class WebhookLog(AggregateRoot):
    """
    Entity representing a webhook delivery log.

    This entity tracks the delivery of webhooks, including the webhook,
    subscription, payload, response, and status.
    """
    webhook_id: EntityId
    subscription_id: Optional[EntityId] = None
    payload: Dict
    http_status: Optional[int] = None
    response_body: Optional[str] = None
    succeeded: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)
