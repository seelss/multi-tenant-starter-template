import logging
from celery import shared_task
from .device_detection import DeviceDetector

logger = logging.getLogger(__name__)

@shared_task
def poll_for_devices():
    """
    Celery task to poll for connected devices once.
    This will be scheduled to run periodically.
    """
    try:
        devices = DeviceDetector.scan_devices()
        logger.info(f"Device polling task completed. Found {len(devices)} Apple devices.")
        return {
            'success': True,
            'devices_found': len(devices),
            'device_list': devices
        }
    except Exception as e:
        logger.error(f"Error in device polling task: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        } 