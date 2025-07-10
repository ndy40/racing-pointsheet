from uuid import UUID

from lato import Query

from modules.notification import notification_module
from modules.notification.exceptions import WebhookNotFoundException
from modules.notification.repository import WebhookRepository
from pointsheet.domain.types import EntityId


class GetWebhook(Query):
    """
    Query to get a webhook by ID.
    """
    webhook_id: EntityId


@notification_module.handler(GetWebhook)
def get_webhook(query: GetWebhook, repo: WebhookRepository):
    """
    Handler for the GetWebhook query.

    Gets a webhook with the specified ID.

    Args:
        query: The GetWebhook query
        repo: The webhook repository

    Returns:
        The webhook with the specified ID

    Raises:
        WebhookNotFoundException: If the webhook with the specified ID doesn't exist
    """
    webhook = repo.find_by_id(query.webhook_id)
    if not webhook:
        raise WebhookNotFoundException()
    return webhook
