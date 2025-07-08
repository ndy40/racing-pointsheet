from typing import Dict, Any, Optional, List

from modules.notification.domain.entity import Webhook
from modules.notification.formatters.base import WebhookFormatter

class DiscordFormatter(WebhookFormatter):
    """Base formatter for Discord webhooks."""
    
    def format_payload(self, webhook: Webhook, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Format a payload for Discord webhooks."""
        # Get webhook config or use defaults
        config = webhook.config or {}
        
        # Create the Discord webhook payload
        discord_payload = {
            "content": self.create_content(webhook, payload, config),
            "username": config.get("username", "PSR"),
            "avatar_url": config.get("avatar_url"),
        }
        
        # Add embeds if configured
        embeds = self.create_embeds(webhook, payload, config)
        if embeds:
            discord_payload["embeds"] = embeds
            
        return discord_payload
    
    def create_content(self, webhook: Webhook, payload: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create the content field for a Discord webhook."""
        # Use a template from config or create a default message
        template = config.get("content_template")
        if template:
            try:
                return template.format(**payload)
            except KeyError:
                # Fallback if template formatting fails
                pass
        
        # Default implementation - should be overridden by subclasses
        event_type = payload.get("event_type", "Unknown")
        return f"New event: {event_type}"
    
    def create_embeds(self, webhook: Webhook, payload: Dict[str, Any], config: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Create embeds for a Discord webhook."""
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