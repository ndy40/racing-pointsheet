from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from modules.notification import WebhookPlatform


class WebhookCreate(BaseModel):
    name: str
    target_url: HttpUrl
    platform: WebhookPlatform
    secret: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class WebhookUpdate(BaseModel):
    name: Optional[str] = None
    target_url: Optional[HttpUrl] = None
    platform: Optional[WebhookPlatform] = None
    secret: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None


class WebhookSubscriptionCreate(BaseModel):
    webhook_id: UUID
    event_type: str
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None


class WebhookResponse(BaseModel):
    id: UUID
    name: str
    target_url: str
    platform: str
    enabled: bool
    created_at: str
    updated_at: Optional[str] = None


class WebhookSubscriptionResponse(BaseModel):
    id: UUID
    webhook_id: UUID
    event_type: str
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None
    created_at: str
    updated_at: Optional[str] = None
