import usb.core
import usb.util
import logging
import time
from datetime import datetime
from core.events import EventSystem

logger = logging.getLogger(__name__)

# Apple's Vendor ID
APPLE_VENDOR_ID = 0x05ac

# Define event types
DEVICE_CONNECTED = 'device_connected'
DEVICE_DISCONNECTED = 'device_disconnected'

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
            
            # Get the serial number as device_id
            if not device.iSerialNumber:
                logger.error(f"No serial number available for device {product}")
                return None
                
            serial = usb.util.get_string(device, device.iSerialNumber)
            if not serial:
                logger.error(f"Failed to retrieve serial number for device {product}")
                return None
                
            # Strip null characters and any whitespace
            device_id = serial.strip().split('\0')[0]
            
            # Port location - simple static identifier
            if hasattr(device, 'port_numbers'):
                port_id = f"b{device.bus}_p{'_'.join([str(p) for p in device.port_numbers])}"
            else:
                port_id = f"b{device.bus}_a{device.address}"
            
            return {
                'manufacturer': manufacturer,
                'name': product,
                'device_id': device_id,
                'port_location': port_id
            }
        except Exception as e:
            logger.error(f"Error extracting device info: {str(e)}")
            return None
    
    # Track devices awaiting trust - shares access with DeviceInfoService
    awaiting_trust_devices = {}

    # Track last scan timestamp to prevent celery task overlaps
    last_scan_time = 0
    
    @classmethod
    def scan_devices(cls):
        """Scan for all connected USB devices and track in memory"""
        import time
        current_time = time.time()
        
        # Skip duplicate scans that happen within less than 0.5 seconds
        # This prevents issues with overlapping celery tasks
        if current_time - cls.last_scan_time < 0.5:
            return list(cls.connected_devices.values())
            
        cls.last_scan_time = current_time
        currently_connected = {}
        
        # Find all connected devices
        try:
            devices = usb.core.find(find_all=True)
            
            for device in devices:
                # Check if it's an Apple device
                if device.idVendor == APPLE_VENDOR_ID:
                    device_info = cls.get_device_info(device)
                    if device_info:
                        # Only include iPhone and iPad devices
                        device_name = device_info['name']
                        if 'iPhone' in device_name or 'iPad' in device_name:
                            device_id = device_info['device_id']
                            currently_connected[device_id] = device_info
                            
                            # Only emit event if:
                            # 1. This is a new device
                            # 2. It's not awaiting trust
                            # 3. We haven't seen it in the last minute
                            first_detection = device_id not in cls.connected_devices
                            not_awaiting_trust = device_id not in cls.awaiting_trust_devices
                            
                            if first_detection and not_awaiting_trust:
                                # Log new device connection with details
                                logger.info(f"New device connected: {device_info}")
                                # Emit device connected event
                                EventSystem.publish(DEVICE_CONNECTED, device_info)
            
            # Check for disconnected devices
            for device_id in list(cls.connected_devices.keys()):
                if device_id not in currently_connected:
                    # Log device disconnection with details
                    disconnected_device = cls.connected_devices[device_id]
                    logger.info(f"Device disconnected: {disconnected_device}")
                    # Emit device disconnected event
                    EventSystem.publish(DEVICE_DISCONNECTED, disconnected_device)
                    del cls.connected_devices[device_id]
                    # Remove from awaiting trust if present
                    cls.awaiting_trust_devices.pop(device_id, None)
            
            # Update connected devices list
            cls.connected_devices = currently_connected
            
            return list(cls.connected_devices.values())
            
        except Exception as e:
            logger.error(f"Error scanning devices: {str(e)}")
            return []

    @classmethod
    def start_polling(cls, interval=1):
        """Start polling for device connections at regular intervals"""
        logger.info(f"Starting device polling with interval of {interval} seconds")
        while True:
            try:
                devices = cls.scan_devices()
                logger.debug(f"Found {len(devices)} connected devices: {devices}")
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("Device polling stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in polling loop: {str(e)}")
                time.sleep(interval)
