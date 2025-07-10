from typing import Optional
from uuid import UUID
from datetime import datetime

from lato import Command, TransactionContext

from modules.notification import notification_module
from modules.notification.domain.entity import WebhookSubscription
from modules.notification.domain.value_objects import WebhookEventType
from modules.notification.exceptions import WebhookNotFoundException, InvalidWebhookConfigurationException
from modules.notification.repository import WebhookRepository, WebhookSubscriptionRepository


class CreateWebhookSubscription(Command):
    """
    Command to create a new webhook subscription.
    """
    webhook_id: UUID
    event_type: str
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None


@notification_module.handler(CreateWebhookSubscription)
def create_webhook_subscription(
    cmd: CreateWebhookSubscription,
    webhook_repo: WebhookRepository,
    subscription_repo: WebhookSubscriptionRepository,
    ctx: TransactionContext
):
    """
    Handler for the CreateWebhookSubscription command.

    Creates a new webhook subscription with the specified parameters.

    Args:
        cmd: The CreateWebhookSubscription command
        webhook_repo: The webhook repository
        subscription_repo: The webhook subscription repository
        ctx: The transaction context

    Returns:
        The created webhook subscription

    Raises:
        WebhookNotFoundException: If the webhook with the specified ID doesn't exist
        InvalidWebhookConfigurationException: If the event type is invalid
    """
    # Verify webhook exists
    webhook = webhook_repo.find_by_id(cmd.webhook_id)
    if not webhook:
        raise WebhookNotFoundException()

    # Verify event type is valid
    try:
        event_type = WebhookEventType(cmd.event_type)
    except ValueError:
        raise InvalidWebhookConfigurationException()

    subscription = WebhookSubscription(
        webhook_id=cmd.webhook_id,
        event_type=event_type,
        resource_type=cmd.resource_type,
        resource_id=cmd.resource_id,
        created_at=datetime.now()
    )

    subscription_repo.add(subscription)

    return subscription
