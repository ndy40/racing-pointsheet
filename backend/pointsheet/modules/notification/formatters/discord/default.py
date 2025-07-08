from typing import Dict, Any

from modules.notification.domain.entity import Webhook
from modules.notification.formatters.discord.base import DiscordFormatter

class DefaultFormatter(DiscordFormatter):
    """Default formatter for Discord webhooks."""
    
    def create_content(self, webhook: Webhook, payload: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create default content based on event type."""
        event_type = payload.get("event_type", "Unknown")
        return f"New event: {event_type}"