from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class DeviceConnectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'device_connector'
    
    def ready(self):
        """Initialize the app and register event handlers"""
        # Import here to avoid circular imports
        from .services import DeviceConnectionService
        from .models import Device
        
        # Clear all device records on startup, but handle the case where table doesn't exist yet
        try:
            Device.objects.all().delete()
        except (OperationalError, ProgrammingError):
            # Table doesn't exist yet, migrations haven't been run
            pass
        
        # Initialize the device connection service
        DeviceConnectionService.initialize()