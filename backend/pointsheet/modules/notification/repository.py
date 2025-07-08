from typing import List, Optional

from lato import Query
from sqlalchemy import select, and_, or_

from modules.notification.data_mappers import WebhookModelMapper, WebhookSubscriptionModelMapper, WebhookLogModelMapper
from modules.notification.domain.entity import Webhook as WebhookEntity
from modules.notification.domain.entity import WebhookSubscription as WebhookSubscriptionEntity
from modules.notification.domain.entity import WebhookLog as WebhookLogEntity
from modules.notification.domain.value_objects import WebhookEventType
from pointsheet.models.notification import Webhook, WebhookSubscription, WebhookLog
from pointsheet.domain.types import EntityId
from pointsheet.repository import AbstractRepository


class WebhookRepository(AbstractRepository[Webhook, WebhookEntity]):
    """
    Repository for Webhook entities.
    """
    mapper_class = WebhookModelMapper
    model_class = WebhookEntity

    def all(self, criteria: Optional[Query] = None) -> List[WebhookEntity]:
        """
        Get all webhooks, optionally filtered by criteria.
        """
        stmt = select(Webhook).order_by(Webhook.created_at.desc())

        if criteria and hasattr(criteria, "enabled") and criteria.enabled is not None:
            # Filter by enabled status
            stmt = stmt.where(Webhook.enabled == criteria.enabled)

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_by_id(self, id: EntityId) -> Optional[WebhookEntity]:
        """
        Find a webhook by ID.
        """
        result = self._session.get(Webhook, id)
        if result:
            return self._map_to_model(result)
        return None

    def find_enabled(self) -> List[WebhookEntity]:
        """
        Find all enabled webhooks.
        """
        stmt = select(Webhook).where(Webhook.enabled == True)
        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def delete(self, id: EntityId) -> None:
        """
        Delete a webhook by ID.
        """
        entity_to_delete = self._session.get(Webhook, id)
        if entity_to_delete:
            self._session.delete(entity_to_delete)


class WebhookSubscriptionRepository(AbstractRepository[WebhookSubscription, WebhookSubscriptionEntity]):
    """
    Repository for WebhookSubscription entities.
    """
    mapper_class = WebhookSubscriptionModelMapper
    model_class = WebhookSubscriptionEntity

    def all(self, criteria: Optional[Query] = None) -> List[WebhookSubscriptionEntity]:
        """
        Get all webhook subscriptions, optionally filtered by criteria.
        """
        stmt = select(WebhookSubscription).order_by(WebhookSubscription.created_at.desc())

        if criteria and hasattr(criteria, "webhook_id") and criteria.webhook_id:
            # Filter by webhook ID
            stmt = stmt.where(WebhookSubscription.webhook_id == criteria.webhook_id)

        if criteria and hasattr(criteria, "event_type") and criteria.event_type:
            # Filter by event type
            stmt = stmt.where(WebhookSubscription.event_type == criteria.event_type.value)

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_by_id(self, id: EntityId) -> Optional[WebhookSubscriptionEntity]:
        """
        Find a webhook subscription by ID.
        """
        result = self._session.get(WebhookSubscription, id)
        if result:
            return self._map_to_model(result)
        return None

    def find_by_event_type(
        self, 
        event_type: WebhookEventType, 
        resource_type: Optional[str] = None,
        resource_id: Optional[EntityId] = None
    ) -> List[WebhookSubscriptionEntity]:
        """
        Find webhook subscriptions for a specific event type, optionally filtered by resource.

        Returns subscriptions in order of specificity:
        1. Exact resource match (event_type + resource_type + resource_id)
        2. Resource type match (event_type + resource_type)
        3. General event type match (event_type only)
        """
        conditions = []

        # Exact resource match
        if resource_type and resource_id:
            conditions.append(
                and_(
                    WebhookSubscription.event_type == event_type.value,
                    WebhookSubscription.resource_type == resource_type,
                    WebhookSubscription.resource_id == str(resource_id)
                )
            )

        # Resource type match
        if resource_type:
            conditions.append(
                and_(
                    WebhookSubscription.event_type == event_type.value,
                    WebhookSubscription.resource_type == resource_type,
                    WebhookSubscription.resource_id.is_(None)
                )
            )

        # General event type match
        conditions.append(
            and_(
                WebhookSubscription.event_type == event_type.value,
                WebhookSubscription.resource_type.is_(None),
                WebhookSubscription.resource_id.is_(None)
            )
        )

        # Combine conditions with OR
        stmt = select(WebhookSubscription).where(or_(*conditions))

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_default_subscriptions(self) -> List[WebhookSubscriptionEntity]:
        """
        Find subscriptions that don't specify a resource_type or resource_id.
        These serve as default fallbacks.
        """
        stmt = select(WebhookSubscription).where(
            WebhookSubscription.resource_type.is_(None),
            WebhookSubscription.resource_id.is_(None)
        )
        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def delete(self, id: EntityId) -> None:
        """
        Delete a webhook subscription by ID.
        """
        entity_to_delete = self._session.get(WebhookSubscription, id)
        if entity_to_delete:
            self._session.delete(entity_to_delete)


class WebhookLogRepository(AbstractRepository[WebhookLog, WebhookLogEntity]):
    """
    Repository for WebhookLog entities.
    """
    mapper_class = WebhookLogModelMapper
    model_class = WebhookLogEntity

    def all(self, criteria: Optional[Query] = None) -> List[WebhookLogEntity]:
        """
        Get all webhook logs, optionally filtered by criteria.
        """
        stmt = select(WebhookLog).order_by(WebhookLog.timestamp.desc())

        if criteria and hasattr(criteria, "webhook_id") and criteria.webhook_id:
            # Filter by webhook ID
            stmt = stmt.where(WebhookLog.webhook_id == criteria.webhook_id)

        if criteria and hasattr(criteria, "subscription_id") and criteria.subscription_id:
            # Filter by subscription ID
            stmt = stmt.where(WebhookLog.subscription_id == criteria.subscription_id)

        if criteria and hasattr(criteria, "succeeded") and criteria.succeeded is not None:
            # Filter by success status
            stmt = stmt.where(WebhookLog.succeeded == criteria.succeeded)

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_by_id(self, id: EntityId) -> Optional[WebhookLogEntity]:
        """
        Find a webhook log by ID.
        """
        result = self._session.get(WebhookLog, id)
        if result:
            return self._map_to_model(result)
        return None

    def delete(self, id: EntityId) -> None:
        """
        Delete a webhook log by ID.
        """
        entity_to_delete = self._session.get(WebhookLog, id)
        if entity_to_delete:
            self._session.delete(entity_to_delete)
