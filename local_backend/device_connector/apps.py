from django.apps import AppConfig


class DeviceConnectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'device_connector'
    
    def ready(self):
        """Initialize the app and register event handlers"""
        # Import here to avoid circular imports
        from .services import DeviceConnectionService
        from .models import Device
        
        # Clear all device records on startup
        Device.objects.all().delete()
        
        # Initialize the device connection service
        DeviceConnectionService.initialize()