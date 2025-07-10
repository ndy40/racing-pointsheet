from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

from lato import Command, TransactionContext

from modules.notification import notification_module
from modules.notification.domain.entity import Webhook
from modules.notification.domain.value_objects import WebhookPlatform
from modules.notification.exceptions import WebhookNotFoundException
from modules.notification.repository import WebhookRepository
from pointsheet.domain.types import EntityId


class UpdateWebhook(Command):
    """
    Command to update an existing webhook.
    """
    webhook_id: UUID
    name: Optional[str] = None
    target_url: Optional[str] = None
    platform: Optional[WebhookPlatform] = None
    secret: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None


@notification_module.handler(UpdateWebhook)
def update_webhook(cmd: UpdateWebhook, repo: WebhookRepository, ctx: TransactionContext):
    """
    Handler for the UpdateWebhook command.

    Updates an existing webhook with the specified parameters.

    Args:
        cmd: The UpdateWebhook command
        repo: The webhook repository
        ctx: The transaction context

    Returns:
        The updated webhook

    Raises:
        WebhookNotFoundException: If the webhook with the specified ID doesn't exist
    """
    webhook = repo.find_by_id(cmd.webhook_id)

    if not webhook:
        raise WebhookNotFoundException()

    # Update fields if provided
    if cmd.name is not None:
        webhook.name = cmd.name
    if cmd.target_url is not None:
        webhook.target_url = cmd.target_url
    if cmd.platform is not None:
        webhook.platform = cmd.platform
    if cmd.secret is not None:
        webhook.secret = cmd.secret
    if cmd.config is not None:
        webhook.config = cmd.config
    if cmd.enabled is not None:
        webhook.enabled = cmd.enabled

    webhook.updated_at = datetime.now()

    repo.update(webhook)

    return webhook
