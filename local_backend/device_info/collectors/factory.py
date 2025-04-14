"""Factory for creating device information collectors."""

import logging
from typing import Dict, Any, Optional

from .base import DeviceInfoCollectorBase
from .ios import IOSDeviceInfoCollector

logger = logging.getLogger(__name__)


class DeviceInfoCollectorFactory:
    """Factory for creating device information collectors.
    
    This factory creates the appropriate collector based on device type,
    environment settings, or other configuration.
    """
    
    @staticmethod
    def create_collector(device_info: Dict[str, Any]) -> DeviceInfoCollectorBase:
        """Create appropriate collector for the given device.
        
        Args:
            device_info: Basic device information dictionary.
            
        Returns:
            An instance of DeviceInfoCollectorBase.
        """
        device_id = device_info.get('device_id', 'unknown')
        device_name = device_info.get('name', '').lower()
        
        # Choose collector based on device name
        if 'iphone' in device_name or 'ipad' in device_name or 'ios' in device_name:
            logger.info(f"Creating iOS collector for device {device_id}")
            return IOSDeviceInfoCollector()
        
        # Default to iOS collector for now
        # In the future, we can add more device type detections and collectors
        logger.info(f"Defaulting to iOS collector for device {device_name} with ID {device_id}")
        return IOSDeviceInfoCollector() 