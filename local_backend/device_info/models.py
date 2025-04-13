from django.db import models
from django.utils import timezone

class DeviceInfo(models.Model):
    """Stores additional information about devices"""
    
    # Device identifier (matches device_id in device_connector)
    device_id = models.CharField(max_length=255, unique=True)
    
    # Additional device information
    imei = models.CharField(max_length=50, blank=True, null=True)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    product_type = models.CharField(max_length=50, blank=True, null=True)
    model_number = models.CharField(max_length=50, blank=True, null=True)
    region_info = models.CharField(max_length=50, blank=True, null=True)
    region_info_human_readable = models.CharField(max_length=255, blank=True, null=True)
    ios_version = models.CharField(max_length=50, blank=True, null=True)
    activation_state = models.CharField(max_length=50, blank=True, null=True)
    findmy_status = models.CharField(max_length=10, blank=True, null=True)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    storage_capacity = models.CharField(max_length=50, blank=True, null=True)
    housing_color = models.CharField(max_length=50, blank=True, null=True)
    
    # Legacy fields - keeping for backward compatibility
    model_identifier = models.CharField(max_length=50, blank=True, null=True)
    battery_level = models.IntegerField(blank=True, null=True)
    storage_total = models.BigIntegerField(blank=True, null=True)  # in bytes
    storage_used = models.BigIntegerField(blank=True, null=True)   # in bytes
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"DeviceInfo for {self.device_id} ({self.model_name or self.product_type or 'Unknown model'})"
    
    @property
    def storage_percentage(self):
        """Calculate storage usage percentage"""
        if self.storage_total and self.storage_used:
            return round((self.storage_used / self.storage_total) * 100, 1)
        return None
