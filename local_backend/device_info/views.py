from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import DeviceInfo

# Create your views here.

@require_http_methods(["GET"])
def device_info_list(request):
    """Return a list of all devices with their additional info"""
    devices = list(DeviceInfo.objects.values(
        'device_id', 'imei', 'serial_number', 'product_type', 'model_number',
        'region_info', 'ios_version', 'model_name', 'storage_capacity',
        'activation_state', 'findmy_status', 'housing_color',
        'battery_level', 'storage_total', 'storage_used', 'last_updated'
    ))
    
    # Add calculated fields
    for device in devices:
        if device['storage_total'] and device['storage_used']:
            device['storage_percentage'] = round((device['storage_used'] / device['storage_total']) * 100, 1)
        else:
            device['storage_percentage'] = None
    
    return JsonResponse({'devices': devices})

@require_http_methods(["GET"])
def device_info_detail(request, device_id):
    """Return detailed info for a specific device"""
    device = get_object_or_404(DeviceInfo, device_id=device_id)
    
    data = {
        'device_id': device.device_id,
        'imei': device.imei,
        'serial_number': device.serial_number,
        'product_type': device.product_type,
        'model_number': device.model_number,
        'region_info': device.region_info,
        'region_info_human_readable': device.region_info_human_readable,
        'ios_version': device.ios_version,
        'activation_state': device.activation_state,
        'findmy_status': device.findmy_status,
        'model_name': device.model_name,
        'storage_capacity': device.storage_capacity,
        'housing_color': device.housing_color,
        'model_identifier': device.model_identifier,
        'battery_level': device.battery_level,
        'storage_total': device.storage_total,
        'storage_used': device.storage_used,
        'storage_percentage': device.storage_percentage,
        'last_updated': device.last_updated
    }
    
    return JsonResponse(data)
