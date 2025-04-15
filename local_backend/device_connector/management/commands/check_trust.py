import subprocess
import time
import shlex
import select
import sys
import traceback
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Checks and potentially initiates the trust pairing process for a connected iOS device using pymobiledevice3.'

    def add_arguments(self, parser):
        parser.add_argument('udid', type=str, help='UDID of the iOS device to check trust status for')

    def handle(self, *args, **options):
        udid = options['udid']
        
        try:
            #self.stdout.write(f"Running command: pymobiledevice3 springboard orientation --udid {udid}")
            
            cmd = f"pymobiledevice3 springboard orientation --udid {udid}"
            process = subprocess.Popen(
                shlex.split(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True, # Keep text mode for simplicity
                # bufsize=1 # Line buffering might still be useful, but select handles responsiveness
            )
            
            # stdout_lines = [] # No longer needed as we don't parse orientation
            stderr_lines = []
            pairing_message_shown = False
            trust_established_early = False # Flag if trust seems okay before command ends

            # Use select for non-blocking reads (works on Unix-like systems)
            streams = [process.stdout, process.stderr]
            
            while process.poll() is None:
                # Wait for data on either stdout or stderr, with a short timeout
                # Adjust timeout as needed, 0.1 seconds is reasonable
                readable, _, _ = select.select(streams, [], [], 0.1) 

                for stream in readable:
                    # Read all available lines from the stream to avoid missing messages
                    while True: 
                        line = stream.readline()
                        if not line: # No more lines available for now or EOF
                            break 

                        line = line.strip()
                        if not line: # Skip empty lines
                            continue

                        if stream == process.stderr:
                            # print(f"STDERR: {line}") # Debugging removed
                            stderr_lines.append(line)
                            # Check for specific messages in stderr
                            if 'user refused to trust this computer' in line.lower():
                                self.stderr.write(self.style.ERROR("User refused to trust this computer"))
                                process.terminate()
                                return # Exit command
                            elif 'waiting user pairing dialog' in line.lower() and not pairing_message_shown:
                                self.stdout.write(self.style.WARNING("Please accept trust pairing on the device..."))
                                pairing_message_shown = True
                            elif 'waiting for user to trust' in line.lower() and not pairing_message_shown:
                                self.stdout.write(self.style.WARNING("Please accept trust pairing on the device..."))
                                pairing_message_shown = True
                            elif 'device not found' in line.lower():
                                self.stderr.write(self.style.ERROR("Device not connected"))
                                process.terminate()
                                return # Exit command
                            # If we see logs like "Creating host key" but no pairing prompt, trust might already exist
                            #elif 'creating host key' in line.lower() and not pairing_message_shown:
                            #    trust_established_early = True 

                        elif stream == process.stdout:
                            # print(f"STDOUT: {line}") # Debugging removed
                            # stdout_lines.append(line) # No longer needed
                            # Check for device not connected in stdout (unlikely but just in case)
                            if 'device is not connected' in line.lower() or 'device not found' in line.lower():
                                self.stderr.write(self.style.ERROR("Device is not connected"))
                                process.terminate() # Terminate if device not found
                                return # Exit command
                            # If stdout produces '0' or '1', trust is definitely established
                            if line.strip() == '0' or line.strip() == '1':
                                trust_established_early = True


                # Check again if process ended after reading
                if process.poll() is not None:
                    break
                
                # No need for time.sleep() here as select provides the timeout

            # After process finishes, read any remaining output using communicate()
            # This ensures we capture everything even if the process exits quickly after the loop
            # We only care about remaining stderr now
            _, remaining_stderr = process.communicate()
            if remaining_stderr:
                stderr_lines.extend(remaining_stderr.strip().split('\n'))

            # Clean up empty strings potentially added by split
            # stdout_lines = [l for l in stdout_lines if l and l.strip()] # Removed
            stderr_lines = [l for l in stderr_lines if l and l.strip()]

            # stdout_str = '\n'.join(stdout_lines).strip() # Removed
            stderr_str = '\n'.join(stderr_lines).strip()
            return_code = process.returncode
            
            # --- Process Results ---

            # Check for explicit refusal first (most important)
            if 'user refused to trust this computer' in stderr_str.lower():
                self.stderr.write(self.style.ERROR("User refused to trust this computer"))
                return

            # Check for device not found error (only need to check stderr now)
            if 'device not found' in stderr_str.lower():
                 self.stderr.write(self.style.ERROR("Device not connected"))
                 return

            # Check if pairing was needed/successful
            pairing_initiated = pairing_message_shown # Use the flag set during real-time monitoring

            # Determine success/failure based on findings
            if trust_established_early and return_code == 0:
                 # If we detected trust early (e.g., saw orientation output or key creation without prompt) and command succeeded
                 self.stdout.write(self.style.SUCCESS("Trust already established with the device."))
                 return
            elif pairing_initiated and return_code == 0:
                 # If pairing was initiated and command exited cleanly (rc=0), assume pairing succeeded.
                 self.stdout.write(self.style.SUCCESS("Trust pairing process completed successfully."))
                 return
            elif pairing_initiated and return_code != 0:
                 # If pairing was initiated but command failed (e.g., timeout waiting for user).
                 # Check stderr for specific timeout messages if available, otherwise generic failure.
                 if "timed out" in stderr_str.lower():
                      self.stderr.write(self.style.ERROR(f"Trust pairing timed out. Please accept the prompt on the device and try again. STDERR: {stderr_str}"))
                 else:
                      self.stderr.write(self.style.ERROR(f"Trust pairing initiated but command failed (code: {return_code}). Check device or logs. STDERR: {stderr_str}"))
                 return
            elif not pairing_initiated and return_code == 0:
                 # Command succeeded without initiating pairing - implies trust was already established.
                 self.stdout.write(self.style.SUCCESS("Trust already established with the device."))
                 return
            elif return_code != 0:
                # General command failure without pairing being initiated
                self.stderr.write(self.style.ERROR(f"Command failed (code: {return_code}). Trust may not be established. STDERR: {stderr_str}"))
                return
            else:
                 # Fallback for unexpected scenarios (e.g., rc=0, no pairing, but unexpected stderr)
                 self.stdout.write(self.style.WARNING(f"Command finished with unclear status (code: {return_code}). STDERR: {stderr_str}"))


        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Error: 'pymobiledevice3' command not found. Make sure it's installed and in your PATH."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
            self.stderr.write(traceback.format_exc()) # Print full traceback for debugging
