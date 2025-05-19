# app_functions.py
import subprocess
import threading

receiver_process = None

def start_receiver():
    global receiver_process
    if receiver_process is None or receiver_process.poll() is not None:
        receiver_process = subprocess.Popen(['python', 'receiver.py'])
        return True
    return False

def stop_receiver():
    global receiver_process
    if receiver_process and receiver_process.poll() is None:
        receiver_process.terminate()
        receiver_process = None
        return True
    return False

def send_files(ip, filepaths):
    # filepaths: list of file paths
    # For each file, call send.py with the IP and file path
    results = []
    for path in filepaths:
        try:
            result = subprocess.run(['python', 'send.py'], input=f"{ip}\n{path}\n", text=True, capture_output=True, timeout=60)
            results.append({'file': path, 'output': result.stdout, 'error': result.stderr})
        except Exception as e:
            results.append({'file': path, 'output': '', 'error': str(e)})
    return results

