import usb.core
import usb.util
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

# Apple's Vendor ID
APPLE_VENDOR_ID = 0x05ac

class DeviceDetector:
    """Service for detecting and managing connected devices"""
    
    # Track connected devices in memory
    connected_devices = {}
    
    @staticmethod
    def get_device_info(device):
        """Extract useful information from a USB device"""
        try:
            manufacturer = usb.util.get_string(device, device.iManufacturer) if device.iManufacturer else "Unknown"
            product = usb.util.get_string(device, device.iProduct) if device.iProduct else "Unknown"
            
            # Generate a unique identifier
            device_id = f"{device.idVendor:04x}:{device.idProduct:04x}-{device.bus}-{device.address}"
            
            # Port location
            port_location = f"Bus {device.bus}, Port {device.port_numbers}" if hasattr(device, 'port_numbers') else f"Bus {device.bus}, Address {device.address}"
            
            return {
                'manufacturer': manufacturer,
                'name': product,
                'device_id': device_id,
                'port_location': port_location
            }
        except Exception as e:
            logger.error(f"Error extracting device info: {str(e)}")
            return None
    
    @classmethod
    def scan_devices(cls):
        """Scan for all connected USB devices and track in memory"""
        currently_connected = {}
        
        # Find all connected devices
        try:
            devices = usb.core.find(find_all=True)
            
            for device in devices:
                # Check if it's an Apple device
                if device.idVendor == APPLE_VENDOR_ID:
                    device_info = cls.get_device_info(device)
                    if device_info:
                        device_id = device_info['device_id']
                        currently_connected[device_id] = device_info
                        
                        # Check if this is a new device
                        if device_id not in cls.connected_devices:
                            logger.info(f"New device detected: {device_info['manufacturer']} {device_info['name']} at {device_info['port_location']}")
            
            # Check for disconnected devices
            for device_id in list(cls.connected_devices.keys()):
                if device_id not in currently_connected:
                    disconnected_device = cls.connected_devices[device_id]
                    logger.info(f"Device disconnected: {disconnected_device['manufacturer']} {disconnected_device['name']} from {disconnected_device['port_location']}")
                    del cls.connected_devices[device_id]
            
            # Update connected devices list
            cls.connected_devices = currently_connected
            
            return list(cls.connected_devices.values())
            
        except Exception as e:
            logger.error(f"Error scanning devices: {str(e)}")
            return []

    @classmethod
    def start_polling(cls, interval=5):
        """Start polling for device connections at regular intervals"""
        logger.info(f"Starting device polling with interval of {interval} seconds")
        while True:
            try:
                devices = cls.scan_devices()
                logger.debug(f"Found {len(devices)} connected devices")
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("Device polling stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in polling loop: {str(e)}")
                time.sleep(interval)
