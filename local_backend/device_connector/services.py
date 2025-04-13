import logging
from django.utils import timezone
from core.events import EventSystem
from device_connector.device_detection import DEVICE_CONNECTED, DEVICE_DISCONNECTED
from .models import Device

logger = logging.getLogger(__name__)

class DeviceConnectionService:
    """Service for managing device connection state in the database"""
    
    @classmethod
    def initialize(cls):
        """Initialize the service by subscribing to device events"""
        logger.info("Initializing DeviceConnectionService")
        EventSystem.subscribe(DEVICE_CONNECTED, cls.handle_device_connected)
        EventSystem.subscribe(DEVICE_DISCONNECTED, cls.handle_device_disconnected)
    
    @classmethod
    def handle_device_connected(cls, device_info):
        """Handle a device connected event by updating the device in the database"""
        logger.info(f"DeviceConnectionService: Processing newly connected device {device_info['device_id']}")
        
        # Update or create device record
        device, created = Device.objects.update_or_create(
            device_id=device_info['device_id'],
            defaults={
                'manufacturer': device_info.get('manufacturer', 'Unknown'),
                'name': device_info.get('name', 'Unknown Device'),
                'port_location': device_info.get('port_location', ''),
                'is_connected': True,
                'last_seen': timezone.now()
            }
        )
        
        if created:
            logger.info(f"Added new device to database: {device}")
        else:
            logger.info(f"Updated existing device in database: {device}")
    
    @classmethod
    def handle_device_disconnected(cls, device_info):
        """Handle a device disconnected event by updating the device in the database"""
        device_id = device_info['device_id']
        logger.info(f"DeviceConnectionService: Device disconnected {device_id}")
        
        try:
            # Mark device as disconnected
            device = Device.objects.get(device_id=device_id)
            device.is_connected = False
            device.last_seen = timezone.now()
            device.save()
            logger.info(f"Marked device as disconnected in database: {device}")
        except Device.DoesNotExist:
            logger.error(f"Tried to mark device {device_id} as disconnected, but it doesn't exist in database") 