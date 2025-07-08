"""
Webhook formatters module.

This module provides backward compatibility for the old webhook formatter API.
New code should use the formatters package instead.
"""

# Re-export classes from the new structure for backward compatibility
from modules.notification.formatters.base import WebhookFormatter
from modules.notification.formatters.factory import DynamicWebhookFormatterFactory
from modules.notification.formatters.discord.base import DiscordFormatter as DiscordWebhookFormatter
from modules.notification.formatters import WebhookFormatterFactory
