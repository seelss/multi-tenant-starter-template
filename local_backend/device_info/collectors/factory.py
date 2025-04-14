"""Factory for creating device information collectors."""

import logging
from typing import Dict, Any, Optional

from .base import DeviceInfoCollectorBase
from .mock import MockDeviceInfoCollector
from .ios import IOSDeviceInfoCollector

logger = logging.getLogger(__name__)


class DeviceInfoCollectorFactory:
    """Factory for creating device information collectors.
    
    This factory creates the appropriate collector based on device type,
    environment settings, or other configuration.
    """
    
    @staticmethod
    def create_collector(device_info: Dict[str, Any], use_mock: bool = False) -> DeviceInfoCollectorBase:
        """Create appropriate collector for the given device.
        
        Args:
            device_info: Basic device information dictionary.
            use_mock: Force using mock collector regardless of device type.
            
        Returns:
            An instance of DeviceInfoCollectorBase.
        """
        device_id = device_info.get('device_id', 'unknown')
        device_name = device_info.get('name', '').lower()
        
        # Force using mock collector if specified
        if use_mock:
            logger.info(f"Creating mock collector for device {device_id} (forced)")
            return MockDeviceInfoCollector()
        
        # Choose collector based on device name
        if 'iphone' in device_name or 'ipad' in device_name or 'ios' in device_name:
            logger.info(f"Creating iOS collector for device {device_id}")
            ios_collector = IOSDeviceInfoCollector()
            
            # Currently the iOS collector is a placeholder and will return None
            # In that case, we'll fall back to the mock collector
            test_result = ios_collector.collect_device_info(device_id, device_info)
            if test_result is not None:
                return ios_collector
                
            logger.warning(f"iOS collector failed for device {device_id}, falling back to mock collector")
            return MockDeviceInfoCollector()
        
        # Default to mock collector
        logger.info(f"Using default mock collector for device {device_name} with ID {device_id}")
        return MockDeviceInfoCollector() 