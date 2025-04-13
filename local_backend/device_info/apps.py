from django.apps import AppConfig


class DeviceInfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'device_info'
    
    def ready(self):
        """Initialize the app and register event handlers"""
        # Import here to avoid circular imports
        from .services import DeviceInfoService
        
        # Initialize the device info service
        DeviceInfoService.initialize()
