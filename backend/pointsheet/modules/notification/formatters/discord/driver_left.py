from typing import Dict, Any

from modules.notification.domain.entity import Webhook
from modules.notification.formatters.discord.base import DiscordFormatter

class DriverLeftFormatter(DiscordFormatter):
    """Formatter for DriverLeftEvent events on Discord."""
    
    def create_content(self, webhook: Webhook, payload: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create content for DriverLeftEvent event."""
        return "🚪 Driver has left an event!"