from typing import Optional, Dict, Any
from datetime import datetime

from lato import Command, TransactionContext

from modules.notification import notification_module
from modules.notification.domain.entity import Webhook
from modules.notification.domain.value_objects import WebhookPlatform
from modules.notification.repository import WebhookRepository


class CreateWebhook(Command):
    """
    Command to create a new webhook.
    """
    name: str
    target_url: str
    platform: WebhookPlatform
    secret: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


@notification_module.handler(CreateWebhook)
def create_webhook(cmd: CreateWebhook, repo: WebhookRepository, ctx: TransactionContext):
    """
    Handler for the CreateWebhook command.
    
    Creates a new webhook with the specified parameters and adds it to the repository.
    
    Args:
        cmd: The CreateWebhook command
        repo: The webhook repository
        ctx: The transaction context
    
    Returns:
        The created webhook
    """
    webhook = Webhook(
        name=cmd.name,
        target_url=cmd.target_url,
        platform=cmd.platform,
        secret=cmd.secret,
        config=cmd.config,
        enabled=True,
        created_at=datetime.now()
    )
    
    repo.add(webhook)
    
    return webhook