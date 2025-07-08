import importlib
import re
from typing import Type

from modules.notification.domain.entity import Webhook
from modules.notification.domain.value_objects import WebhookPlatform
from modules.notification.formatters.base import WebhookFormatter

class DynamicWebhookFormatterFactory:
    """
    Factory for dynamically creating webhook formatters.
    
    This factory creates the appropriate formatter for a given webhook platform and event type.
    """
    
    @staticmethod
    def create_formatter(platform: WebhookPlatform, event_type: str) -> WebhookFormatter:
        """
        Create a formatter for the specified platform and event type.
        
        Args:
            platform: The webhook platform
            event_type: The event type
            
        Returns:
            A formatter for the specified platform and event type
            
        Raises:
            ValueError: If the platform is not supported
        """
        platform_value = platform.value.lower()
        
        # Convert event type to snake_case (e.g., SeriesCreated -> series_created)
        event_name = re.sub(r'(?<!^)(?=[A-Z])', '_', event_type).lower()
        
        # Try to import the specific formatter
        try:
            module_path = f"modules.notification.formatters.{platform_value}.{event_name}"
            module = importlib.import_module(module_path)
            
            # Look for a class that ends with "Formatter"
            formatter_class = None
            for attr_name in dir(module):
                if attr_name.endswith("Formatter"):
                    formatter_class = getattr(module, attr_name)
                    break
            
            if formatter_class:
                return formatter_class()
        except (ImportError, AttributeError):
            # If specific formatter not found, try to use the default formatter
            try:
                module_path = f"modules.notification.formatters.{platform_value}.default"
                module = importlib.import_module(module_path)
                default_formatter_class = getattr(module, "DefaultFormatter")
                return default_formatter_class()
            except (ImportError, AttributeError):
                pass
        
        # If no formatter found, raise error
        raise ValueError(f"Unsupported webhook platform: {platform} or event type: {event_type}")