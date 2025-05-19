import subprocess
import threading
import os
from datetime import datetime

RECEIVER_PROCESS = None

def log_activity(message):
    with open('activity.log', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

def start_receiver():
    global RECEIVER_PROCESS
    if RECEIVER_PROCESS is None or RECEIVER_PROCESS.poll() is not None:
        RECEIVER_PROCESS = subprocess.Popen(['python', 'receiver.py'])
        log_activity("Receiver started")
        return True
    return False

def stop_receiver():
    global RECEIVER_PROCESS
    if RECEIVER_PROCESS and RECEIVER_PROCESS.poll() is None:
        RECEIVER_PROCESS.terminate()
        RECEIVER_PROCESS = None
        log_activity("Receiver stopped")
        return True
    return False

def send_files(ip, file_paths):
    results = []
    for path in file_paths:
        try:
            result = subprocess.run(
                ['python', 'sender.py', ip, path],
                capture_output=True,
                text=True,
                timeout=60
            )
            results.append({
                'file': os.path.basename(path),
                'output': result.stdout,
                'error': result.stderr
            })
            log_activity(f"Sent {os.path.basename(path)} to {ip}")
        except Exception as e:
            results.append({
                'file': os.path.basename(path),
                'output': '',
                'error': str(e)
            })
            log_activity(f"Failed to send {os.path.basename(path)}: {str(e)}")
    return results
