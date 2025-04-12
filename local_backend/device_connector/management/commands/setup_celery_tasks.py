from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class Command(BaseCommand):
    help = 'Set up periodic Celery tasks for device polling'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=1,
            help='Polling interval in seconds'
        )

    def handle(self, *args, **options):
        interval_seconds = options['interval']
        
        # Create or get interval schedule
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=interval_seconds,
            period=IntervalSchedule.SECONDS,
        )
        
        # Create or update the periodic task
        task, created = PeriodicTask.objects.update_or_create(
            name='Poll for USB devices',
            defaults={
                'task': 'device_connector.tasks.poll_for_devices',
                'interval': schedule,
                'enabled': True,
            }
        )
        
        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(
                f'{action} periodic task to poll for devices every {interval_seconds} second(s)'
            )
        ) 