from typing import Dict, List, Any

from modules.notification.domain.entity import Webhook as WebhookEntity
from modules.notification.domain.entity import WebhookSubscription as WebhookSubscriptionEntity
from modules.notification.domain.entity import WebhookLog as WebhookLogEntity
from modules.notification.domain.value_objects import WebhookPlatform, WebhookEventType
from modules.notification.models import Webhook, WebhookSubscription, WebhookLog
from pointsheet.repository import DataMapper


class WebhookModelMapper(DataMapper[Webhook, WebhookEntity]):
    """
    Mapper for converting between Webhook model and entity.
    """

    def to_domain_model(self, model: Webhook) -> WebhookEntity:
        """
        Convert a Webhook model to a WebhookEntity.
        """
        return WebhookEntity(
            id=model.id,
            name=model.name,
            target_url=model.target_url,
            platform=WebhookPlatform(model.platform),
            secret=model.secret,
            config=model.config,
            enabled=model.enabled,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def to_db_entity(self, entity: WebhookEntity) -> Webhook:
        """
        Convert a WebhookEntity to a Webhook model.
        """
        return Webhook(
            id=entity.id,
            name=entity.name,
            target_url=entity.target_url,
            platform=entity.platform.value,
            secret=entity.secret,
            config=entity.config,
            enabled=entity.enabled,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )


class WebhookSubscriptionModelMapper(DataMapper[WebhookSubscription, WebhookSubscriptionEntity]):
    """
    Mapper for converting between WebhookSubscription model and entity.
    """

    def to_domain_model(self, model: WebhookSubscription) -> WebhookSubscriptionEntity:
        """
        Convert a WebhookSubscription model to a WebhookSubscriptionEntity.
        """
        return WebhookSubscriptionEntity(
            id=model.id,
            webhook_id=model.webhook_id,
            event_type=WebhookEventType(model.event_type),
            resource_type=model.resource_type,
            resource_id=model.resource_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def to_db_entity(self, entity: WebhookSubscriptionEntity) -> WebhookSubscription:
        """
        Convert a WebhookSubscriptionEntity to a WebhookSubscription model.
        """
        return WebhookSubscription(
            id=entity.id,
            webhook_id=entity.webhook_id,
            event_type=entity.event_type.value,
            resource_type=entity.resource_type,
            resource_id=entity.resource_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )


class WebhookLogModelMapper(DataMapper[WebhookLog, WebhookLogEntity]):
    """
    Mapper for converting between WebhookLog model and entity.
    """

    def to_domain_model(self, model: WebhookLog) -> WebhookLogEntity:
        """
        Convert a WebhookLog model to a WebhookLogEntity.
        """
        return WebhookLogEntity(
            id=model.id,
            webhook_id=model.webhook_id,
            subscription_id=model.subscription_id,
            payload=model.payload,
            http_status=model.http_status,
            response_body=model.response_body,
            succeeded=model.succeeded,
            timestamp=model.timestamp
        )

    def to_db_entity(self, entity: WebhookLogEntity) -> WebhookLog:
        """
        Convert a WebhookLogEntity to a WebhookLog model.
        """
        return WebhookLog(
            id=entity.id,
            webhook_id=entity.webhook_id,
            subscription_id=entity.subscription_id,
            payload=entity.payload,
            http_status=entity.http_status,
            response_body=entity.response_body,
            succeeded=entity.succeeded,
            timestamp=entity.timestamp
        )
