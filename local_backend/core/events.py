import logging
from typing import Dict, List, Callable, Any

logger = logging.getLogger(__name__)

class EventSystem:
    """A simple publish/subscribe event system for the application"""
    
    # Dictionary to store subscribers for each event type
    _subscribers: Dict[str, List[Callable]] = {}
    
    @classmethod
    def subscribe(cls, event_type: str, callback: Callable) -> None:
        """Subscribe to an event type with a callback function"""
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event '{event_type}'")
        
    @classmethod
    def unsubscribe(cls, event_type: str, callback: Callable) -> None:
        """Unsubscribe a callback from an event type"""
        if event_type in cls._subscribers and callback in cls._subscribers[event_type]:
            cls._subscribers[event_type].remove(callback)
            logger.debug(f"Unsubscribed from event '{event_type}'")
    
    @classmethod
    def publish(cls, event_type: str, data: Any = None) -> None:
        """Publish an event with optional data to all subscribers"""
        if event_type not in cls._subscribers:
            return
            
        logger.debug(f"Publishing event '{event_type}' with data: {data}")
        for callback in cls._subscribers[event_type]:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Error in event subscriber for '{event_type}': {str(e)}") 