from django.core.management.base import BaseCommand
from device_connector.device_detection import DeviceDetector
import logging

class Command(BaseCommand):
    help = 'Start polling for device connections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=5,
            help='Polling interval in seconds'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        self.stdout.write(self.style.SUCCESS(f'Starting device polling with interval of {interval} seconds'))
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('device_polling.log')
            ]
        )
        
        try:
            # Start the polling service
            DeviceDetector.start_polling(interval=interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Device polling stopped by user'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in device polling: {str(e)}')) 