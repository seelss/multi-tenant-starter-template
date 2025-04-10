from django.shortcuts import render
from django.http import JsonResponse
from .models import Device
from .device_detection import DeviceDetector

def device_list(request):
    """Return a list of all devices as JSON"""
    devices = Device.objects.all().values(
        'id', 'manufacturer', 'name', 'port_location', 
        'is_connected', 'first_connected', 'last_seen'
    )
    return JsonResponse({'devices': list(devices)})

def connected_devices(request):
    """Return a list of currently connected devices as JSON"""
    devices = Device.objects.filter(is_connected=True).values(
        'id', 'manufacturer', 'name', 'port_location', 
        'first_connected', 'last_seen'
    )
    return JsonResponse({'devices': list(devices)})

def scan_now(request):
    """Trigger an immediate device scan and return results"""
    devices = DeviceDetector.scan_devices()
    device_data = [
        {
            'id': device.id,
            'manufacturer': device.manufacturer,
            'name': device.name,
            'port_location': device.port_location,
            'first_connected': device.first_connected,
            'last_seen': device.last_seen
        }
        for device in devices
    ]
    return JsonResponse({'devices': device_data})
