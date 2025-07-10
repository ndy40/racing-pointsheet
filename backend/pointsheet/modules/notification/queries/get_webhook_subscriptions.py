from typing import List
from uuid import UUID

from lato import Query

from modules.notification import notification_module
from modules.notification.domain.entity import WebhookSubscription
from modules.notification.repository import WebhookSubscriptionRepository


class GetWebhookSubscriptions(Query):
    """
    Query to get all subscriptions for a webhook.
    """
    webhook_id: UUID


@notification_module.handler(GetWebhookSubscriptions)
def get_webhook_subscriptions(
    query: GetWebhookSubscriptions,
    repo: WebhookSubscriptionRepository
) -> List[WebhookSubscription]:
    """
    Handler for the GetWebhookSubscriptions query.
    
    Gets all subscriptions for a webhook with the specified ID.
    
    Args:
        query: The GetWebhookSubscriptions query
        repo: The webhook subscription repository
    
    Returns:
        A list of webhook subscriptions
    """
    return repo.all(query)