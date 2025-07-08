"""
Webhook formatters package.

This package contains formatters for different webhook platforms and event types.
"""

from modules.notification.formatters.base import WebhookFormatter
from modules.notification.formatters.factory import DynamicWebhookFormatterFactory
from modules.notification.formatters.discord.base import DiscordFormatter as DiscordWebhookFormatter

# Define WebhookFormatterFactory directly in __init__.py to avoid circular imports
from modules.notification.domain.value_objects import WebhookPlatform

class WebhookFormatterFactory:
    """
    Factory for creating webhook formatters.

    This factory creates the appropriate formatter for a given webhook platform.
    For backward compatibility only. New code should use DynamicWebhookFormatterFactory.
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

__all__ = ["DynamicWebhookFormatterFactory", "WebhookFormatter", "DiscordWebhookFormatter", "WebhookFormatterFactory"]
