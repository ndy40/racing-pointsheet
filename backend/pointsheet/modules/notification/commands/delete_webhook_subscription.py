from uuid import UUID

from lato import Command, TransactionContext

from modules.notification import notification_module
from modules.notification.exceptions import WebhookSubscriptionNotFoundException
from modules.notification.repository import WebhookSubscriptionRepository


class DeleteWebhookSubscription(Command):
    """
    Command to delete a webhook subscription.
    """
    subscription_id: UUID


@notification_module.handler(DeleteWebhookSubscription)
def delete_webhook_subscription(
    cmd: DeleteWebhookSubscription,
    repo: WebhookSubscriptionRepository,
    ctx: TransactionContext
):
    """
    Handler for the DeleteWebhookSubscription command.

    Deletes a webhook subscription with the specified ID.

    Args:
        cmd: The DeleteWebhookSubscription command
        repo: The webhook subscription repository
        ctx: The transaction context

    Returns:
        True if the webhook subscription was deleted

    Raises:
        WebhookSubscriptionNotFoundException: If the webhook subscription with the specified ID doesn't exist
    """
    subscription = repo.find_by_id(cmd.subscription_id)

    if not subscription:
        raise WebhookSubscriptionNotFoundException()

    repo.delete(subscription.id)

    return True
