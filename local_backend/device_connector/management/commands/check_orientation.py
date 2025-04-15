import subprocess
import time
import shlex
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Runs pymobiledevice3 springboard orientation command and returns the orientation value (0 or 1)'

    def add_arguments(self, parser):
        parser.add_argument('udid', type=str, help='UDID of the iOS device to check')

    def handle(self, *args, **options):
        udid = options['udid']
        
        try:
            self.stdout.write(f"Running command: pymobiledevice3 springboard orientation --udid {udid}")
            
            # Start process with real-time output monitoring
            cmd = f"pymobiledevice3 springboard orientation --udid {udid}"
            process = subprocess.Popen(
                shlex.split(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            
            stdout_lines = []
            stderr_lines = []
            pairing_message_shown = False
            
            # Capture output in real-time
            while True:
                # Check if process has ended
                if process.poll() is not None:
                    break
                    
                # Read stderr line by line
                stderr_line = process.stderr.readline()
                if stderr_line:
                    stderr_lines.append(stderr_line.strip())
                    # Check for user refusing to trust
                    if 'user refused to trust this computer' in stderr_line.lower():
                        self.stderr.write(self.style.ERROR("User refused to trust this computer"))
                        process.terminate()
                        return
                    # Check for pairing dialog
                    elif 'waiting user pairing dialog' in stderr_line.lower() and not pairing_message_shown:
                        self.stdout.write(self.style.WARNING("Please accept trust pairing on the device..."))
                        pairing_message_shown = True
                    # Check for host key creation (which typically happens before pairing)
                    elif 'creating host key & certificate' in stderr_line.lower() and not pairing_message_shown:
                        self.stdout.write(self.style.WARNING("Trust pairing will be required, please watch your device..."))
                        pairing_message_shown = True
                    # Check for device not found
                    elif 'device not found' in stderr_line.lower():
                        self.stderr.write(self.style.ERROR("Device is not connected"))
                        process.terminate()
                        return
                
                # Read stdout line by line
                stdout_line = process.stdout.readline()
                if stdout_line:
                    stdout_lines.append(stdout_line.strip())
                
                # Small sleep to prevent high CPU usage
                time.sleep(0.1)
            
            # Get remaining output
            remaining_stdout, remaining_stderr = process.communicate()
            if remaining_stdout:
                stdout_lines.extend(remaining_stdout.strip().split('\n'))
            if remaining_stderr:
                stderr_lines.extend(remaining_stderr.strip().split('\n'))
            
            # Process results
            stdout_str = '\n'.join(stdout_lines).strip()
            stderr_str = '\n'.join(stderr_lines).strip()
            return_code = process.returncode
            
            # Debug output
            self.stdout.write(f"Return code: {return_code}")
            
            # Check for user refusing to trust in the accumulated stderr
            if 'user refused to trust this computer' in stderr_str.lower():
                self.stderr.write(self.style.ERROR("User refused to trust this computer"))
                return
            
            # Check for other errors
            if return_code != 0:
                self.stderr.write(self.style.ERROR(f"Command failed: {stderr_str}"))
                return
                
            # Process the output
            if not stdout_str:
                # Check if it was a pairing initialization that succeeded
                if ('creating host key & certificate' in stderr_str.lower() or 
                    'waiting user pairing dialog' in stderr_str.lower()):
                    self.stdout.write(self.style.SUCCESS("Trust pairing has succeeded"))
                    return
                elif stderr_str:
                    self.stdout.write(self.style.WARNING(f"Command running: {stderr_str}"))
                else:
                    self.stderr.write(self.style.ERROR("Empty output received from command"))
                return
            
            # Check if device is not connected in stdout (unlikely but just in case)
            if 'device is not connected' in stdout_str.lower() or 'device not found' in stdout_str.lower():
                self.stderr.write(self.style.ERROR("Device is not connected"))
                return
            
            # Extract the integer value from output
            try:
                # Try to find and parse the integer in the output
                for word in stdout_str.split():
                    if word.isdigit() and (word == '0' or word == '1'):
                        # Output success message instead of the integer
                        self.stdout.write(self.style.SUCCESS("Trust pairing has succeeded"))
                        return
                
                # If we couldn't find a 0 or 1, output the raw result
                self.stderr.write(self.style.ERROR(f"Unexpected output format: '{stdout_str}' (length: {len(stdout_str)})"))
            except ValueError:
                self.stderr.write(self.style.ERROR(f"Could not parse orientation value from: '{stdout_str}'"))
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}")) 