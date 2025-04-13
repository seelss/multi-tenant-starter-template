import logging
import random
from django.utils import timezone
from core.events import EventSystem
from device_connector.device_detection import DEVICE_CONNECTED, DEVICE_DISCONNECTED
from .models import DeviceInfo

logger = logging.getLogger(__name__)

class DeviceInfoService:
    """Service for collecting and managing additional device information"""
    
    @classmethod
    def initialize(cls):
        """Initialize the service by subscribing to device events"""
        logger.info("Initializing DeviceInfoService")
        EventSystem.subscribe(DEVICE_CONNECTED, cls.handle_device_connected)
        EventSystem.subscribe(DEVICE_DISCONNECTED, cls.handle_device_disconnected)
    
    @classmethod
    def handle_device_connected(cls, device_info):
        """Handle a device connected event"""
        logger.info(f"DeviceInfoService: Processing newly connected device {device_info['device_id']}")
        
        # Collect additional information for this device
        cls.collect_device_info(device_info)
    
    @classmethod
    def handle_device_disconnected(cls, device_info):
        """Handle a device disconnected event"""
        logger.info(f"DeviceInfoService: Device disconnected {device_info['device_id']}")
        # We could mark the device info as stale or do other cleanup here
    
    @classmethod
    def collect_device_info(cls, device_info):
        """Collect additional information about a device
        
        In a real implementation, this would run commands to query the device.
        For this example, we'll just generate some sample data.
        """
        device_id = device_info['device_id']
        logger.info(f"Collecting additional info for device {device_id}")
        
        try:
            # For demonstration, we'll use random sample data
            # In a real implementation, you would run commands to query the device
            
            # Determine if it's an iPhone or iPad based on the device name
            is_iphone = 'iPhone' in device_info['name']
            device_type = 'iPhone' if is_iphone else 'iPad'
            
            # iPhone model options
            iphone_models = [
                {'product_type': 'iPhone14,3', 'model_name': 'iPhone 13 Pro Max', 'model_number': 'MLH63'},
                {'product_type': 'iPhone15,3', 'model_name': 'iPhone 14 Pro Max', 'model_number': 'MQ8V3'},
                {'product_type': 'iPhone16,2', 'model_name': 'iPhone 15 Pro Max', 'model_number': 'MU2A3'},
            ]
            
            # iPad model options
            ipad_models = [
                {'product_type': 'iPad13,1', 'model_name': 'iPad Air (4th gen)', 'model_number': 'MYGW2'},
                {'product_type': 'iPad14,5', 'model_name': 'iPad Pro 12.9-inch (5th gen)', 'model_number': 'MHNF3'},
                {'product_type': 'iPad15,2', 'model_name': 'iPad Pro 11-inch (4th gen)', 'model_number': 'MNXD3'},
            ]
            
            # Select random model data based on device type
            model_data = random.choice(iphone_models if is_iphone else ipad_models)
            
            # Region info options
            region_info_options = [
                {'region_info': 'LL/A', 'region_info_human_readable': 'United States and Canada'},
                {'region_info': 'ZA/A', 'region_info_human_readable': 'Hong Kong, Macao, and Taiwan'},
                {'region_info': 'FD/A', 'region_info_human_readable': 'Switzerland and Liechtenstein'},
            ]
            region_data = random.choice(region_info_options)
            
            # Color options
            colors = ['Space Gray', 'Silver', 'Gold', 'Pacific Blue', 'Graphite', 'Sierra Blue', 'Deep Purple']
            
            # Storage options
            storage_options = ['64GB', '128GB', '256GB', '512GB', '1TB']
            
            # Generate sample device info
            sample_info = {
                # Use the model data selected above
                'product_type': model_data['product_type'],
                'model_name': model_data['model_name'],
                'model_number': model_data['model_number'],
                
                # Region info
                'region_info': region_data['region_info'],
                'region_info_human_readable': region_data['region_info_human_readable'],
                
                # Generate other fields
                'imei': ''.join([str(random.randint(0, 9)) for _ in range(15)]),
                'serial_number': ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12)),
                'ios_version': f"17.{random.randint(0, 7)}.{random.randint(0, 3)}",
                'activation_state': random.choice(['Activated', 'Unactivated']),
                'findmy_status': random.choice(['on', 'off']),
                'housing_color': random.choice(colors),
                'storage_capacity': random.choice(storage_options),
                
                # Legacy fields
                'model_identifier': model_data['product_type'],  # For backward compatibility
                'battery_level': random.randint(10, 100),
                'storage_total': int(int(random.choice(storage_options[1:-1]).replace('GB', '')) * 1024 * 1024 * 1024),  # Convert GB to bytes
                'storage_used': random.randint(20, 110) * 1024 * 1024 * 1024,  # 20-110GB in bytes
            }
            
            # Update or create device info record
            device_info_obj, created = DeviceInfo.objects.update_or_create(
                device_id=device_id,
                defaults={
                    **sample_info,
                    'last_updated': timezone.now()
                }
            )
            
            logger.info(f"{'Created' if created else 'Updated'} device info for {device_id}: {sample_info}")
            
            return device_info_obj
            
        except Exception as e:
            logger.error(f"Error collecting device info for {device_id}: {str(e)}")
            return None 