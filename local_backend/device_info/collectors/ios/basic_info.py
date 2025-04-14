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
import json
import subprocess
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
        
        try:
            # Use pymobiledevice3 to get device information
            cmd = ["pymobiledevice3", "lockdown", "info", "--udid", device_id]
            logger.info(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            device_data = json.loads(result.stdout)
            
            # Extract the relevant information from the command output
            imei = device_data.get("InternationalMobileEquipmentIdentity", "")
            serial_number = device_data.get("SerialNumber", "")
            product_type = device_data.get("ProductType", "")
            model_number = device_data.get("ModelNumber", "")
            region_info = device_data.get("RegionInfo", "")
            ios_version = device_data.get("ProductVersion", "")
            activation_state = device_data.get("ActivationState", "")
            
            # Determine Find My status based on the fm-account-masked value
            findmy_status = "off"
            non_volatile_ram = device_data.get("NonVolatileRAM", {})
            fm_account_masked = non_volatile_ram.get("fm-account-masked", "<>")
            
            # If fm-account-masked has content inside <> tags, Find My is on
            if fm_account_masked != "<>" and len(fm_account_masked) > 2:
                findmy_status = "on"
            
            basic_info = {
                'imei': imei,
                'serial_number': serial_number,
                'product_type': product_type,
                'model_number': model_number,
                'region_info': region_info,
                'ios_version': ios_version,
                'activation_state': activation_state,
                'findmy_status': findmy_status,
            }
            
            logger.info(f"Successfully collected basic info for iOS device {device_id}")
            return basic_info
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running pymobiledevice3 command: {e}")
            logger.error(f"Command output: {e.stdout}")
            logger.error(f"Command error: {e.stderr}")
            return self._get_fallback_info(device_id)
            
        except Exception as e:
            logger.error(f"Unexpected error collecting device info: {str(e)}")
            return self._get_fallback_info(device_id)
    
    def _get_fallback_info(self, device_id: str) -> Dict[str, Any]:
        """Return fallback placeholder information when collection fails.
        
        Args:
            device_id: The unique identifier of the device.
            
        Returns:
            Dictionary containing placeholder device information.
        """
        logger.warning(f"Using fallback placeholder info for device {device_id}")
        return {
            'imei': "Not Found",
            'serial_number': "Not Found",
            'product_type': "Not Found",
            'model_number': "Not Found",
            'region_info': "Not Found",
            'ios_version': "Not Found",
            'activation_state': "Unknown",
            'findmy_status': "Unknown",
        } 