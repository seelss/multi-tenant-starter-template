import subprocess
import shlex
import select
import sys
import traceback
import logging
from enum import Enum, auto

logger = logging.getLogger(__name__)

class TrustStatus(Enum):
    """Represents the trust status of an iOS device."""
    TRUSTED = auto()              # Device is already trusted or trust established successfully
    PAIRING_SUCCESSFUL = auto()   # Pairing prompt was shown and likely accepted (command succeeded)
    PAIRING_REQUIRED = auto()     # Pairing prompt is actively being shown
    PAIRING_REFUSED = auto()      # User explicitly refused the trust prompt
    DEVICE_NOT_FOUND = auto()     # Device with the specified UDID was not found/connected
    TIMEOUT = auto()              # Command timed out (e.g., waiting for user interaction)
    COMMAND_NOT_FOUND = auto()    # pymobiledevice3 command is not available
    ERROR = auto()                # An unexpected error occurred during the check

def check_ios_trust(udid: str) -> TrustStatus:
    """
    Checks the trust status of a connected iOS device using pymobiledevice3.

    This function runs 'pymobiledevice3 springboard orientation' primarily to trigger
    the trust dialog if necessary. It monitors the command's output to determine
    the trust status.

    Args:
        udid: The UDID of the iOS device.

    Returns:
        A TrustStatus enum member indicating the result.
    """
    logger.info(f"Checking iOS trust status for device: {udid}")
    
    try:
        cmd = f"pymobiledevice3 springboard orientation --udid {udid}"
        process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        
        stderr_lines = []
        pairing_message_shown = False
        trust_established_early = False 

        streams = [process.stdout, process.stderr]
        
        while process.poll() is None:
            readable, _, _ = select.select(streams, [], [], 0.1) 

            for stream in readable:
                while True: 
                    line = stream.readline()
                    if not line: break 
                    line = line.strip()
                    if not line: continue

                    if stream == process.stderr:
                        logger.debug(f"STDERR [{udid}]: {line}")
                        stderr_lines.append(line)
                        if 'user refused to trust this computer' in line.lower():
                            logger.warning(f"User refused trust for device: {udid}")
                            process.terminate()
                            return TrustStatus.PAIRING_REFUSED
                        elif 'waiting user pairing dialog' in line.lower() and not pairing_message_shown:
                            logger.info(f"Pairing dialog shown for device: {udid}. Waiting for user...")
                            pairing_message_shown = True
                        elif 'waiting for user to trust' in line.lower() and not pairing_message_shown:
                            logger.info(f"Pairing dialog shown for device: {udid}. Waiting for user...")
                            pairing_message_shown = True
                        elif 'device not found' in line.lower():
                            logger.error(f"Device not found during trust check: {udid}")
                            process.terminate()
                            return TrustStatus.DEVICE_NOT_FOUND
                        #elif 'creating host key' in line.lower() and not pairing_message_shown:
                        #    trust_established_early = True # This might be too optimistic

                    elif stream == process.stdout:
                        logger.debug(f"STDOUT [{udid}]: {line}")
                        if 'device is not connected' in line.lower() or 'device not found' in line.lower():
                            logger.error(f"Device not found during trust check (stdout): {udid}")
                            process.terminate()
                            return TrustStatus.DEVICE_NOT_FOUND
                        if line.strip() == '0' or line.strip() == '1':
                            # Receiving orientation means trust is established
                            trust_established_early = True

            if process.poll() is not None:
                break

        # Process finished, get remaining output and final status
        _, remaining_stderr = process.communicate()
        if remaining_stderr:
            stderr_lines.extend(remaining_stderr.strip().split('\n'))
        
        stderr_lines = [l for l in stderr_lines if l and l.strip()]
        stderr_str = '\n'.join(stderr_lines).strip()
        return_code = process.returncode

        logger.info(f"Trust check command finished for {udid}. RC: {return_code}, Pairing Prompt Shown: {pairing_message_shown}, Trust Early: {trust_established_early}")
        logger.debug(f"Final STDERR [{udid}]: {stderr_str}")

        # --- Interpret Results ---
        if 'user refused to trust this computer' in stderr_str.lower():
            return TrustStatus.PAIRING_REFUSED
        if 'device not found' in stderr_str.lower():
             return TrustStatus.DEVICE_NOT_FOUND

        pairing_initiated = pairing_message_shown

        if trust_established_early and return_code == 0:
             logger.info(f"Trust already established for device: {udid}")
             return TrustStatus.TRUSTED
        elif pairing_initiated and return_code == 0:
             logger.info(f"Trust pairing process completed successfully for device: {udid}")
             return TrustStatus.PAIRING_SUCCESSFUL # Or TRUSTED, depending on desired semantics
        elif pairing_initiated and return_code != 0:
             if "timed out" in stderr_str.lower():
                  logger.warning(f"Trust pairing timed out for device: {udid}")
                  return TrustStatus.TIMEOUT # Specific timeout status
             else:
                  logger.error(f"Trust pairing initiated but command failed for {udid} (RC: {return_code}). STDERR: {stderr_str}")
                  return TrustStatus.ERROR # Generic error during pairing
        elif not pairing_initiated and return_code == 0:
             logger.info(f"Trust already established for device (no pairing needed): {udid}")
             return TrustStatus.TRUSTED
        elif return_code != 0:
            logger.error(f"Trust check command failed for {udid} (RC: {return_code}). STDERR: {stderr_str}")
            return TrustStatus.ERROR
        else:
             # Should not happen often (RC=0, no pairing, no early trust indication)
             logger.warning(f"Trust check for {udid} finished with unclear status (RC: {return_code}). Assuming trusted.")
             return TrustStatus.TRUSTED # Default to trusted if command succeeds without error/pairing

    except FileNotFoundError:
        logger.error("'pymobiledevice3' command not found. Make sure it's installed and in PATH.")
        return TrustStatus.COMMAND_NOT_FOUND
    except Exception as e:
        logger.error(f"An unexpected error occurred during trust check for {udid}: {e}", exc_info=True)
        # logger.error(traceback.format_exc()) # Redundant if exc_info=True
        return TrustStatus.ERROR

# Example usage (for testing purposes)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ios_trust_manager.py <udid>")
        sys.exit(1)
    
    # Basic logging setup for standalone testing
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_udid = sys.argv[1]
    status = check_ios_trust(test_udid)
    print(f"Trust status for {test_udid}: {status.name}")
