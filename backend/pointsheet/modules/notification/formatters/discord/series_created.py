from typing import Dict, Any

from modules.notification.domain.entity import Webhook
from modules.notification.formatters.discord.base import DiscordFormatter

class SeriesCreatedFormatter(DiscordFormatter):
    """Formatter for SeriesCreated events on Discord."""
    
    def create_content(self, webhook: Webhook, payload: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create content for SeriesCreated event."""
        return "🏁 New racing series created!"