import sys
import traceback
import logging # Use logging consistent with the manager
from django.core.management.base import BaseCommand
from ...ios_trust_manager import check_ios_trust, TrustStatus # Import the new function and enum

class Command(BaseCommand):
    help = 'Checks and potentially initiates the trust pairing process for a connected iOS device using pymobiledevice3.'

    def add_arguments(self, parser):
        parser.add_argument('udid', type=str, help='UDID of the iOS device to check trust status for')

    def handle(self, *args, **options):
        udid = options['udid']
        self.stdout.write(f"Checking trust status for device: {udid}...")

        # Call the refactored function
        status = check_ios_trust(udid)

        # Translate the status enum to user-friendly output
        if status == TrustStatus.TRUSTED:
            self.stdout.write(self.style.SUCCESS("Trust already established with the device."))
        elif status == TrustStatus.PAIRING_SUCCESSFUL:
            self.stdout.write(self.style.SUCCESS("Trust pairing process completed successfully."))
        elif status == TrustStatus.PAIRING_REQUIRED:
             # Note: The check_ios_trust function currently doesn't return this status directly,
             # as it waits for the command to finish. This case is less likely here.
             self.stdout.write(self.style.WARNING("Pairing prompt is active. Please accept trust on the device."))
        elif status == TrustStatus.PAIRING_REFUSED:
            self.stderr.write(self.style.ERROR("User refused to trust this computer."))
        elif status == TrustStatus.DEVICE_NOT_FOUND:
            self.stderr.write(self.style.ERROR("Device not connected or not found."))
        elif status == TrustStatus.TIMEOUT:
             self.stderr.write(self.style.ERROR("Trust pairing timed out. Please accept the prompt on the device and try again."))
        elif status == TrustStatus.COMMAND_NOT_FOUND:
             self.stderr.write(self.style.ERROR("Error: 'pymobiledevice3' command not found. Make sure it's installed and in your PATH."))
        elif status == TrustStatus.ERROR:
             self.stderr.write(self.style.ERROR("An unexpected error occurred during the trust check. Check logs for details."))
        else:
             # Fallback for any unexpected status
             self.stderr.write(self.style.ERROR(f"Received unexpected trust status: {status}"))
