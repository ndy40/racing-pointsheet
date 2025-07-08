import abc
from abc import abstractmethod
from typing import Dict, Any

from modules.notification.domain.entity import Webhook

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