import logging
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from .device_detection import DeviceDetector

logger = logging.getLogger(__name__)

# Store the last known state
last_device_state = None

@shared_task(
    bind=True,
    soft_time_limit=30,  # 30 second timeout
    max_retries=3,       # Retry up to 3 times
    rate_limit='1/5s'    # Only allow one execution per 5 seconds
)
def poll_for_devices(self):
    """
    Celery task to poll for connected devices once.
    This will be scheduled to run periodically.
    """
    global last_device_state
    
    try:
        devices = DeviceDetector.scan_devices()
        
        # Only log if there's a change in devices
        if devices != last_device_state:
            if last_device_state is None:
                logger.info(f"Initial device scan completed. Found {len(devices)} Apple devices.")
            else:
                old_count = len(last_device_state)
                new_count = len(devices)
                if new_count > old_count:
                    logger.info(f"New device(s) detected. Total devices: {new_count}")
                elif new_count < old_count:
                    logger.info(f"Device(s) disconnected. Total devices: {new_count}")
                else:
                    logger.info("Device configuration changed")
            
            last_device_state = devices
            
        return {
            'success': True,
            'devices_found': len(devices),
            'device_list': devices
        }
    except SoftTimeLimitExceeded:
        logger.warning("Device polling task exceeded time limit")
        raise self.retry(countdown=60)  # Retry after 1 minute
    except Exception as e:
        logger.error(f"Error in device polling task: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        } 