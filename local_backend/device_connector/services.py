import logging
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.events import EventSystem
from device_connector.device_detection import DEVICE_CONNECTED, DEVICE_DISCONNECTED
from .models import Device

logger = logging.getLogger(__name__)
channel_layer = get_channel_layer()

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
        
        # Determine device type based on manufacturer
        device_type = 'ios' if device_info.get('manufacturer', '').lower() == 'apple inc.' else 'other'
        
        # Update or create device record
        device, created = Device.objects.update_or_create(
            device_id=device_info['device_id'],
            defaults={
                'manufacturer': device_info.get('manufacturer', 'Unknown'),
                'name': device_info.get('name', 'Unknown Device'),
                'port_location': device_info.get('port_location', ''),
                'device_type': device_type,
                'is_connected': True,
                'last_seen': timezone.now()
            }
        )
        
        if created:
            logger.info(f"Added new device to database: {device}")
        else:
            logger.info(f"Updated existing device in database: {device}")
            
        # Broadcast device list update to all clients via WebSocket
        try:
            async_to_sync(channel_layer.group_send)(
                "device_updates",
                {
                    "type": "device_list_update",
                    "action": "connected",
                    "device_id": device_info['device_id']
                }
            )
        except Exception as e:
            logger.error(f"Error broadcasting device connected event: {str(e)}")
    
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
            
            # Broadcast device list update to all clients via WebSocket
            try:
                async_to_sync(channel_layer.group_send)(
                    "device_updates",
                    {
                        "type": "device_list_update",
                        "action": "disconnected",
                        "device_id": device_id
                    }
                )
            except Exception as e:
                logger.error(f"Error broadcasting device disconnected event: {str(e)}")
                
        except Device.DoesNotExist:
            logger.error(f"Tried to mark device {device_id} as disconnected, but it doesn't exist in database") 