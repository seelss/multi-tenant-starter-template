"""Basic iOS device information collector.

This module handles the collection of basic iOS device information such as:
- imei
- serial_number
- product_type
- model_number
- region_info
- ios_version
- activation_state
- findmy_status
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BasicInfoCollector:
    """Collects basic information from iOS devices."""
    
    def collect_basic_info(self, device_id: str) -> Dict[str, Any]:
        """Collect basic device information.
        
        Args:
            device_id: The unique identifier of the device.
            
        Returns:
            Dictionary containing basic device information.
        """
        logger.info(f"Collecting basic information for iOS device {device_id}")
        
        # This is a placeholder implementation
        # In the future, this will use proper iOS CLI tools to collect real device information
        basic_info = {
            'imei': f"PLACEHOLDER-IMEI-{device_id[:8]}",
            'serial_number': f"PLACEHOLDER-SN-{device_id[:8]}",
            'product_type': "iPhone11,6",  # Placeholder
            'model_number': "MT0H2LL/A",   # Placeholder
            'region_info': "LL/A",         # Placeholder
            'ios_version': "17.4",         # Placeholder
            'activation_state': "Activated", # Placeholder
            'findmy_status': "off",        # Placeholder
        }
        
        logger.info(f"Collected basic info for iOS device {device_id}")
        return basic_info 