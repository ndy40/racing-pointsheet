from typing import Dict, Any

from modules.notification.domain.entity import Webhook
from modules.notification.formatters.discord.base import DiscordFormatter

class SeriesClosedFormatter(DiscordFormatter):
    """Formatter for SeriesClosed events on Discord."""
    
    def create_content(self, webhook: Webhook, payload: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create content for SeriesClosed event."""
        return "🏁 Racing series has closed!"