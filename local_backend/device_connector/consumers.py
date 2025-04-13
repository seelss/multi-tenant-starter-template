import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Device
from device_info.models import DeviceInfo

logger = logging.getLogger(__name__)

class DeviceConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for device updates"""
    
    async def connect(self):
        """Connect to the websocket and join device updates group"""
        await self.channel_layer.group_add(
            "device_updates",
            self.channel_name
        )
        await self.accept()
        logger.info(f"WebSocket client connected: {self.channel_name}")
        
        # Send initial list of connected devices
        devices = await self.get_connected_devices()
        await self.send(text_data=json.dumps({
            'type': 'device_list',
            'devices': devices
        }))
    
    async def disconnect(self, close_code):
        """Disconnect from the websocket and leave device updates group"""
        await self.channel_layer.group_discard(
            "device_updates",
            self.channel_name
        )
        logger.info(f"WebSocket client disconnected: {self.channel_name}")
    
    async def receive(self, text_data):
        """Handle messages from the websocket"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'get_devices':
                # Send current device list when requested
                devices = await self.get_connected_devices()
                await self.send(text_data=json.dumps({
                    'type': 'device_list',
                    'devices': devices
                }))
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {str(e)}")
    
    async def device_update(self, event):
        """Forward device update events to the websocket"""
        # Forward the event data to the WebSocket
        await self.send(text_data=json.dumps(event))
    
    async def device_list_update(self, event):
        """Send updated device list to the client"""
        devices = await self.get_connected_devices()
        await self.send(text_data=json.dumps({
            'type': 'device_list',
            'devices': devices
        }))
    
    @database_sync_to_async
    def get_connected_devices(self):
        """Get a list of all connected devices with their device info"""
        devices = []
        
        # Query all connected devices
        connected_devices = Device.objects.filter(is_connected=True)
        
        for device in connected_devices:
            # Get device info if available
            device_data = {
                'id': device.device_id,
                'type': 'smartphone',  # Assuming all are smartphones for now
                'status': 'online',
                'lastConnected': device.last_seen.isoformat(),
                'model': device.name,
            }
            
            # Try to get additional device info
            try:
                device_info = DeviceInfo.objects.get(device_id=device.device_id)
                
                # Map device info fields to frontend format
                device_data.update({
                    'model': device_info.model_name or device_info.product_type or device.name,
                    'storage': device_info.storage_capacity or 'Unknown',
                    'color': device_info.housing_color or 'Unknown',
                    'imei': device_info.imei or 'Unknown',
                    'serialNumber': device_info.serial_number or 'Unknown',
                    'batteryHealth': f"{device_info.battery_level}%" if device_info.battery_level else 'Unknown',
                    'iosVersion': device_info.ios_version or 'Unknown',
                    'activationStatus': device_info.activation_state or 'Unknown',
                    'findMyStatus': device_info.findmy_status or 'Unknown',
                    'region': device_info.region_info or 'Unknown',
                })
            except DeviceInfo.DoesNotExist:
                # Fill with default values if no additional info is available
                device_data.update({
                    'storage': 'Unknown',
                    'color': 'Unknown',
                    'imei': 'Unknown',
                    'serialNumber': 'Unknown',
                    'batteryHealth': 'Unknown',
                    'iosVersion': 'Unknown',
                    'activationStatus': 'Unknown',
                    'findMyStatus': 'Unknown',
                    'region': 'Unknown',
                })
            
            devices.append(device_data)
        
        return devices 