import subprocess
import time
import shlex
import select
import sys
import traceback # Added for better error reporting
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs pymobiledevice3 springboard orientation command and returns the orientation value (0 or 1)'

    def add_arguments(self, parser):
        parser.add_argument('udid', type=str, help='UDID of the iOS device to check')

    def handle(self, *args, **options):
        udid = options['udid']
        
        try:
            self.stdout.write(f"Running command: pymobiledevice3 springboard orientation --udid {udid}")
            
            cmd = f"pymobiledevice3 springboard orientation --udid {udid}"
            process = subprocess.Popen(
                shlex.split(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True, # Keep text mode for simplicity
                # bufsize=1 # Line buffering might still be useful, but select handles responsiveness
            )
            
            stdout_lines = []
            stderr_lines = []
            pairing_message_shown = False

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
                            print(f"STDERR: {line}") # Debugging
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
                        
                        elif stream == process.stdout:
                            print(f"STDOUT: {line}") # Debugging
                            stdout_lines.append(line)
                            # Check for device not connected in stdout (unlikely but just in case)
                            if 'device is not connected' in line.lower() or 'device not found' in line.lower():
                                self.stderr.write(self.style.ERROR("Device is not connected"))
                                process.terminate() # Terminate if device not found
                                return # Exit command
                
                # Check again if process ended after reading
                if process.poll() is not None:
                    break
                
                # No need for time.sleep() here as select provides the timeout

            # After process finishes, read any remaining output using communicate()
            # This ensures we capture everything even if the process exits quickly after the loop
            remaining_stdout, remaining_stderr = process.communicate()
            if remaining_stdout:
                stdout_lines.extend(remaining_stdout.strip().split('\n'))
            if remaining_stderr:
                stderr_lines.extend(remaining_stderr.strip().split('\n'))

            # Clean up empty strings potentially added by split
            stdout_lines = [l for l in stdout_lines if l and l.strip()]
            stderr_lines = [l for l in stderr_lines if l and l.strip()]

            stdout_str = '\n'.join(stdout_lines).strip()
            stderr_str = '\n'.join(stderr_lines).strip()
            return_code = process.returncode
            
            # Debug output
            self.stdout.write(f"--- Final Output ---")
            self.stdout.write(f"Return code: {return_code}")
            self.stdout.write(f"Final STDOUT:\n{stdout_str if stdout_str else '<empty>'}")
            self.stdout.write(f"Final STDERR:\n{stderr_str if stderr_str else '<empty>'}")
            self.stdout.write(f"--------------------")
            
            # --- Process Results ---

            # Check for explicit refusal first
            if 'user refused to trust this computer' in stderr_str.lower():
                self.stderr.write(self.style.ERROR("User refused to trust this computer"))
                return

            # Check for device not found error
            if 'device not found' in stderr_str.lower() or 'device not found' in stdout_str.lower():
                 self.stderr.write(self.style.ERROR("Device not connected"))
                 return

            # Check if pairing was needed/successful
            pairing_initiated = 'waiting user pairing dialog' in stderr_str.lower() or 'waiting for user to trust' in stderr_str.lower()
            
            # Check if orientation value (0 or 1) is present in stdout
            orientation_value = None
            for word in stdout_str.split():
                if word.isdigit() and (word == '0' or word == '1'):
                    orientation_value = word
                    break

            # Determine success/failure based on findings
            if orientation_value is not None:
                # If we got the orientation value, trust is established.
                self.stdout.write(self.style.SUCCESS(f"Trust established. Device orientation: {orientation_value}"))
                return
            elif pairing_initiated and return_code == 0:
                 # If pairing was initiated and command exited cleanly (rc=0), assume pairing succeeded but orientation wasn't read this time.
                 # This might happen if the command only pairs on the first run.
                 self.stdout.write(self.style.SUCCESS("Trust pairing process completed successfully. Re-run command if needed to get orientation."))
                 return
            elif pairing_initiated and return_code != 0:
                 # If pairing was initiated but command failed, it might be timeout or other issue.
                 self.stderr.write(self.style.ERROR(f"Trust pairing initiated but command failed (code: {return_code}). Check device. STDERR: {stderr_str}"))
                 return
            elif return_code != 0:
                # General command failure
                self.stderr.write(self.style.ERROR(f"Command failed with return code {return_code}. STDERR: {stderr_str}"))
                return
            elif not stdout_str and not stderr_str:
                 # Command ran successfully but produced no output? Unlikely for this command.
                 self.stdout.write(self.style.WARNING("Command finished successfully with no output."))
            elif not stdout_str and stderr_str:
                 # Command succeeded (rc=0) but only produced stderr (likely informational logs)
                 self.stdout.write(self.style.SUCCESS(f"Command finished successfully. Logs: {stderr_str}"))
            else:
                 # Fallback for unexpected successful output
                 self.stderr.write(self.style.ERROR(f"Command finished with unexpected output. STDOUT: '{stdout_str}', STDERR: '{stderr_str}'"))


        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Error: 'pymobiledevice3' command not found. Make sure it's installed and in your PATH."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
            self.stderr.write(traceback.format_exc()) # Print full traceback for debugging
