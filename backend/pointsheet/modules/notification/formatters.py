import abc
from abc import abstractmethod
from typing import Dict, Any, Optional

from modules.notification.domain.entity import Webhook
from modules.notification.domain.value_objects import WebhookPlatform


class WebhookFormatter(abc.ABC):
    """
    Abstract base class for webhook formatters.
    
    This class defines the interface for formatting webhook payloads
    for different platforms.
    """
    
    @abstractmethod
    def format_payload(self, webhook: Webhook, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a payload for a specific webhook platform.
        
        Args:
            webhook: The webhook configuration
            payload: The original event payload
            
        Returns:
            A formatted payload suitable for the specific platform
        """
        pass


class DiscordWebhookFormatter(WebhookFormatter):
    """
    Formatter for Discord webhooks.
    
    This formatter creates payloads according to Discord's webhook API:
    https://discord.com/developers/docs/resources/webhook#execute-webhook
    """
    
    def format_payload(self, webhook: Webhook, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a payload for Discord webhooks.
        
        Args:
            webhook: The webhook configuration
            payload: The original event payload
            
        Returns:
            A formatted payload suitable for Discord webhooks
        """
        # Get webhook config or use defaults
        config = webhook.config or {}
        
        # Create the Discord webhook payload
        discord_payload = {
            "content": self._create_content(payload, config),
            "username": config.get("username", "PSR"),
            "avatar_url": config.get("avatar_url"),
        }
        
        # Add embeds if configured
        embeds = self._create_embeds(payload, config)
        if embeds:
            discord_payload["embeds"] = embeds
            
        return discord_payload
    
    def _create_content(self, payload: Dict[str, Any], config: Dict[str, Any]) -> str:
        """
        Create the content field for a Discord webhook.
        
        Args:
            payload: The original event payload
            config: The webhook configuration
            
        Returns:
            A string for the content field
        """
        # Use a template from config or create a default message
        template = config.get("content_template")
        if template:
            try:
                return template.format(**payload)
            except KeyError:
                # Fallback if template formatting fails
                pass
        
        # Default content based on event type
        event_type = payload.get("event_type", "Unknown")
        
        if "driver_id" in payload and "event_id" in payload:
            if event_type == "DriverJoinedEvent":
                return f"🏎️ Driver has joined an event!"
            elif event_type == "DriverLeftEvent":
                return f"🚪 Driver has left an event!"
        
        if "series_id" in payload:
            if event_type == "SeriesCreated":
                return f"🏁 New racing series created!"
            elif event_type == "SeriesUpdated":
                return f"📝 Racing series updated!"
            elif event_type == "SeriesDeleted":
                return f"🗑️ Racing series deleted!"
            elif event_type == "SeriesStarted":
                return f"🏁 Racing series has started!"
            elif event_type == "SeriesClosed":
                return f"🏁 Racing series has closed!"
        
        if "event_id" in payload:
            if event_type == "EventScheduleAdded":
                return f"📅 New event scheduled!"
            elif event_type == "RaceResultUploaded":
                return f"🏆 Race results uploaded!"
            elif event_type == "EventDeleted":
                return f"🗑️ Event deleted!"
        
        # Generic fallback
        return f"New event: {event_type}"
    
    def _create_embeds(self, payload: Dict[str, Any], config: Dict[str, Any]) -> Optional[list]:
        """
        Create embeds for a Discord webhook.
        
        Args:
            payload: The original event payload
            config: The webhook configuration
            
        Returns:
            A list of embed objects or None
        """
        # Use embeds from config if provided
        if "embeds" in config:
            return config["embeds"]
        
        # Create a default embed based on the event type
        event_type = payload.get("event_type", "Unknown")
        
        # Basic embed with event details
        embed = {
            "title": f"Event: {event_type}",
            "color": 0x00BFFF,  # Deep Sky Blue
            "fields": []
        }
        
        # Add relevant fields based on payload content
        for key, value in payload.items():
            if key != "event_type" and value is not None:
                # Skip complex nested objects
                if not isinstance(value, (dict, list)):
                    embed["fields"].append({
                        "name": key,
                        "value": str(value),
                        "inline": True
                    })
        
        return [embed] if embed["fields"] else None


class WebhookFormatterFactory:
    """
    Factory for creating webhook formatters.
    
    This factory creates the appropriate formatter for a given webhook platform.
    """
    
    @staticmethod
    def create_formatter(platform: WebhookPlatform) -> WebhookFormatter:
        """
        Create a formatter for the specified platform.
        
        Args:
            platform: The webhook platform
            
        Returns:
            A formatter for the specified platform
            
        Raises:
            ValueError: If the platform is not supported
        """
        if platform == WebhookPlatform.DISCORD:
            return DiscordWebhookFormatter()
        # Add more formatters for other platforms here
        # elif platform == WebhookPlatform.SLACK:
        #     return SlackWebhookFormatter()
        # elif platform == WebhookPlatform.TELEGRAM:
        #     return TelegramWebhookFormatter()
        # elif platform == WebhookPlatform.GENERIC_HTTP:
        #     return GenericHttpWebhookFormatter()
        else:
            raise ValueError(f"Unsupported webhook platform: {platform}")