from uuid import UUID
from datetime import datetime

from lato import Command, TransactionContext

from modules.notification import notification_module
from modules.notification.exceptions import WebhookNotFoundException
from modules.notification.repository import WebhookRepository


class ToggleWebhook(Command):
    """
    Command to toggle the enabled status of a webhook.
    """
    webhook_id: UUID


@notification_module.handler(ToggleWebhook)
def toggle_webhook(cmd: ToggleWebhook, repo: WebhookRepository, ctx: TransactionContext):
    """
    Handler for the ToggleWebhook command.

    Toggles the enabled status of a webhook with the specified ID.

    Args:
        cmd: The ToggleWebhook command
        repo: The webhook repository
        ctx: The transaction context

    Returns:
        A tuple of (webhook_id, enabled) indicating the new enabled status

    Raises:
        WebhookNotFoundException: If the webhook with the specified ID doesn't exist
    """
    webhook = repo.find_by_id(cmd.webhook_id)

    if not webhook:
        raise WebhookNotFoundException()

    webhook.enabled = not webhook.enabled
    webhook.updated_at = datetime.now()

    repo.update(webhook)

    return webhook.id, webhook.enabled
