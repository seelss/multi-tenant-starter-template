"""Base classes for device information collectors."""

import abc
from typing import Dict, Any, Optional


class DeviceInfoCollectorBase(abc.ABC):
    """Base class for device information collectors.
    
    All device information collectors should inherit from this class
    and implement the collect_device_info method.
    """
    
    @abc.abstractmethod
    def collect_device_info(self, device_id: str, device_base_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Collect device information.
        
        Args:
            device_id: The unique identifier of the device.
            device_base_info: Basic device information already available.
            
        Returns:
            A dictionary with the collected device information or None if collection failed.
        """
        pass 