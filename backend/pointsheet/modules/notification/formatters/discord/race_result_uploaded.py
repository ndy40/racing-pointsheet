from typing import Dict, Any

from modules.notification.domain.entity import Webhook
from modules.notification.formatters.discord.base import DiscordFormatter

class RaceResultUploadedFormatter(DiscordFormatter):
    """Formatter for RaceResultUploaded events on Discord."""
    
    def create_content(self, webhook: Webhook, payload: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create content for RaceResultUploaded event."""
        return "🏆 Race results uploaded!"