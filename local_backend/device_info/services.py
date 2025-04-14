import logging
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.events import EventSystem
from device_connector.device_detection import DEVICE_CONNECTED, DEVICE_DISCONNECTED
from .models import DeviceInfo
from .collectors.factory import DeviceInfoCollectorFactory

logger = logging.getLogger(__name__)
channel_layer = get_channel_layer()

class DeviceInfoService:
    """Service for collecting and managing additional device information"""
    
    @classmethod
    def initialize(cls):
        """Initialize the service by subscribing to device events"""
        logger.info("Initializing DeviceInfoService")
        EventSystem.subscribe(DEVICE_CONNECTED, cls.handle_device_connected)
        EventSystem.subscribe(DEVICE_DISCONNECTED, cls.handle_device_disconnected)
    
    @classmethod
    def handle_device_connected(cls, device_info):
        """Handle a device connected event"""
        logger.info(f"DeviceInfoService: Processing newly connected device {device_info['device_id']}")
        
        # Collect additional information for this device
        cls.collect_device_info(device_info)
    
    @classmethod
    def handle_device_disconnected(cls, device_info):
        """Handle a device disconnected event"""
        logger.info(f"DeviceInfoService: Device disconnected {device_info['device_id']}")
        # We could mark the device info as stale or do other cleanup here
    
    @classmethod
    def collect_device_info(cls, device_info):
        """Collect additional information about a device
        
        Uses the appropriate collector to gather device information.
        """
        device_id = device_info['device_id']
        logger.info(f"Collecting additional info for device {device_id}")
        
        try:
            # Create appropriate collector for this device
            collector = DeviceInfoCollectorFactory.create_collector(device_info)
            
            # Collect device information
            collected_info = collector.collect_device_info(device_id, device_info)
            
            if collected_info is None:
                logger.error(f"Failed to collect information for device {device_id}")
                return None
                
            # Update or create device info record
            device_info_obj, created = DeviceInfo.objects.update_or_create(
                device_id=device_id,
                defaults={
                    **collected_info,
                    'last_updated': timezone.now()
                }
            )
            
            logger.info(f"{'Created' if created else 'Updated'} device info for {device_id}")
            
            # Broadcast device info update to all clients via WebSocket
            try:
                async_to_sync(channel_layer.group_send)(
                    "device_updates",
                    {
                        "type": "device_list_update",
                        "action": "device_info_updated",
                        "device_id": device_id
                    }
                )
                logger.info(f"Sent device info update notification for {device_id}")
            except Exception as e:
                logger.error(f"Error broadcasting device info update: {str(e)}")
            
            return device_info_obj
            
        except Exception as e:
            logger.error(f"Error collecting device info for {device_id}: {str(e)}")
            return None 