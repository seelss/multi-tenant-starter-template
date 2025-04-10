from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'name', 'port_location', 'is_connected', 'last_seen')
    list_filter = ('manufacturer', 'is_connected')
    search_fields = ('manufacturer', 'name', 'port_location', 'device_id')
    readonly_fields = ('device_id', 'first_connected', 'last_seen')
