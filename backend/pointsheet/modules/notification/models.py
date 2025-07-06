from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, JSON, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from pointsheet.models.base import BaseModel
from pointsheet.domain.types import EntityId, uuid_default
from pointsheet.models.custom_types import EntityIdType


class Webhook(BaseModel):
    """
    Database model for webhooks.
    """
    __tablename__ = "webhooks"

    id: Mapped[EntityId] = mapped_column(EntityIdType, primary_key=True, default=uuid_default())
    name: Mapped[str] = mapped_column(String, nullable=True)
    target_url: Mapped[str] = mapped_column(String, nullable=False)
    platform: Mapped[str] = mapped_column(String, nullable=False)
    secret: Mapped[str] = mapped_column(String, nullable=True)
    config: Mapped[dict] = mapped_column(JSON, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class WebhookSubscription(BaseModel):
    """
    Database model for webhook subscriptions.
    """
    __tablename__ = "webhook_subscriptions"

    id: Mapped[EntityId] = mapped_column(EntityIdType, primary_key=True, default=uuid_default())
    webhook_id: Mapped[EntityId] = mapped_column(EntityIdType, ForeignKey("webhooks.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    resource_type: Mapped[str] = mapped_column(String, nullable=True)
    resource_id: Mapped[EntityId] = mapped_column(EntityIdType, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class WebhookLog(BaseModel):
    """
    Database model for webhook logs.
    """
    __tablename__ = "webhook_logs"

    id: Mapped[EntityId] = mapped_column(EntityIdType, primary_key=True, default=uuid_default())
    webhook_id: Mapped[EntityId] = mapped_column(EntityIdType, ForeignKey("webhooks.id"), nullable=False)
    subscription_id: Mapped[EntityId] = mapped_column(EntityIdType, ForeignKey("webhook_subscriptions.id"), nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    http_status: Mapped[int] = mapped_column(Integer, nullable=True)
    response_body: Mapped[str] = mapped_column(Text, nullable=True)
    succeeded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
