from uuid import UUID

from lato import Command, TransactionContext

from modules.notification import notification_module
from modules.notification.exceptions import WebhookNotFoundException
from modules.notification.repository import WebhookRepository


class DeleteWebhook(Command):
    """
    Command to delete a webhook.
    """
    webhook_id: UUID


@notification_module.handler(DeleteWebhook)
def delete_webhook(cmd: DeleteWebhook, repo: WebhookRepository, ctx: TransactionContext):
    """
    Handler for the DeleteWebhook command.

    Deletes a webhook with the specified ID.

    Args:
        cmd: The DeleteWebhook command
        repo: The webhook repository
        ctx: The transaction context

    Returns:
        True if the webhook was deleted

    Raises:
        WebhookNotFoundException: If the webhook with the specified ID doesn't exist
    """
    webhook = repo.find_by_id(cmd.webhook_id)

    if not webhook:
        raise WebhookNotFoundException()

    repo.delete(webhook.id)

    return True
