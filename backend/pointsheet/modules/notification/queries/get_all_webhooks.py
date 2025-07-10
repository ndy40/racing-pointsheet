from typing import Optional, List

from lato import Query

from modules.notification import notification_module
from modules.notification.domain.entity import Webhook
from modules.notification.repository import WebhookRepository


class GetAllWebhooks(Query):
    """
    Query to get all webhooks.
    """
    enabled: Optional[bool] = None


@notification_module.handler(GetAllWebhooks)
def get_all_webhooks(query: GetAllWebhooks, repo: WebhookRepository) -> List[Webhook]:
    """
    Handler for the GetAllWebhooks query.
    
    Gets all webhooks, optionally filtered by enabled status.
    
    Args:
        query: The GetAllWebhooks query
        repo: The webhook repository
    
    Returns:
        A list of webhooks
    """
    return repo.all(query)