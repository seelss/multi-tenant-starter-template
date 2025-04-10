import usb.core
import usb.util
import logging
import time
from datetime import datetime
from django.utils import timezone
from .models import Device

logger = logging.getLogger(__name__)

# Apple's Vendor ID
APPLE_VENDOR_ID = 0x05ac

class DeviceDetector:
    """Service for detecting and managing connected devices"""
    
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
        """Scan for all connected USB devices and update the database"""
        connected_device_ids = set()
        
        # Find all connected devices
        try:
            devices = usb.core.find(find_all=True)
            
            for device in devices:
                # Check if it's an Apple device
                if device.idVendor == APPLE_VENDOR_ID:
                    device_info = cls.get_device_info(device)
                    if device_info:
                        # Update or create device in database
                        device_obj, created = Device.objects.update_or_create(
                            device_id=device_info['device_id'],
                            defaults={
                                'manufacturer': device_info['manufacturer'],
                                'name': device_info['name'],
                                'port_location': device_info['port_location'],
                                'is_connected': True,
                                'last_seen': timezone.now()
                            }
                        )
                        
                        connected_device_ids.add(device_info['device_id'])
                        
                        if created:
                            logger.info(f"New device detected: {device_info['manufacturer']} {device_info['name']} at {device_info['port_location']}")
            
            # Mark devices no longer connected as disconnected
            Device.objects.filter(is_connected=True).exclude(device_id__in=connected_device_ids).update(
                is_connected=False,
                last_seen=timezone.now()
            )
            
            return Device.objects.filter(is_connected=True)
            
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