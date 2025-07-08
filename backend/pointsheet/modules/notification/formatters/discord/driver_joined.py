from typing import Dict, Any

from modules.notification.domain.entity import Webhook
from modules.notification.formatters.discord.base import DiscordFormatter

class DriverJoinedFormatter(DiscordFormatter):
    """Formatter for DriverJoinedEvent events on Discord."""
    
    def create_content(self, webhook: Webhook, payload: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create content for DriverJoinedEvent event."""
        return "🏎️ Driver has joined an event!"