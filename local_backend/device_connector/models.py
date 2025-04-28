from django.db import models
from django.utils import timezone

class Device(models.Model):
    manufacturer = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    port_location = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=50, default='ios')  # Adding the missing field with default value
    is_connected = models.BooleanField(default=True)
    first_connected = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.manufacturer} - {self.name or 'Unknown'} ({self.device_id})"
