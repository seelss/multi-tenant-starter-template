from django.apps import AppConfig
from django.db.utils import OperationalError


class DeviceConnectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'device_connector'
    
    def ready(self):
        """Initialize the app and register event handlers"""
        # Import here to avoid circular imports
        from .services import DeviceConnectionService
        from .models import Device
        from .device_detection import DeviceDetector
        
        try:
            # Mark all devices as disconnected on startup
            Device.objects.all().update(is_connected=False)
            
            # Clear the awaiting_trust_devices dictionary to ensure fresh trust status
            DeviceDetector.awaiting_trust_devices.clear()
        except OperationalError:
            # If the table doesn't exist yet, that's fine - it will be created by migrations
            pass
        
        # Initialize the device connection service
        DeviceConnectionService.initialize()