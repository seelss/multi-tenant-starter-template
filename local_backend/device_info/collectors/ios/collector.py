"""Main iOS device information collector.

This module integrates the specialized collectors and resolvers
to provide comprehensive iOS device information.
"""

import logging
from typing import Dict, Any, Optional

from ..base import DeviceInfoCollectorBase
from .basic_info import BasicInfoCollector
from .model_resolver import ModelResolver
from .region_resolver import RegionResolver

logger = logging.getLogger(__name__)


class IOSDeviceInfoCollector(DeviceInfoCollectorBase):
    """iOS device information collector.
    
    This collector communicates with iOS devices to collect information
    using the appropriate CLI tools and resolvers.
    """
    
    def __init__(self):
        """Initialize the collector with specialized components."""
        self.basic_info_collector = BasicInfoCollector()
        self.model_resolver = ModelResolver()
        self.region_resolver = RegionResolver()
    
    def collect_device_info(self, device_id: str, device_base_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Collect iOS device information.
        
        Args:
            device_id: The unique identifier of the device.
            device_base_info: Basic device information already available.
            
        Returns:
            A dictionary with the collected device information or None if collection failed.
        """
        logger.info(f"Collecting information for iOS device {device_id}")
        
        try:
            # Collect basic device information
            basic_info = self.basic_info_collector.collect_basic_info(device_id)
            
            # Extract model number and region info from basic info
            model_number = basic_info.get('model_number', '')
            region_info = basic_info.get('region_info', '')
            
            # Resolve detailed model information
            model_info = self.model_resolver.resolve_model_info(model_number)
            
            # Resolve region information
            region_info_human_readable = self.region_resolver.resolve_region_info(region_info)
            
            # Combine all information
            device_info = {
                **basic_info,
                'region_info_human_readable': region_info_human_readable,
                'model_name': model_info['model_name'],
                'storage_capacity': model_info['storage_capacity'],
                'housing_color': model_info['housing_color'],
            }
            
            logger.info(f"Successfully collected info for iOS device {device_id}")
            return device_info
            
        except Exception as e:
            logger.error(f"Error collecting iOS device info for {device_id}: {str(e)}")
            return None 