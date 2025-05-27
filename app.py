from flask import Flask, render_template, request, jsonify
import os
import re
import app_functions
import subprocess

app = Flask(__name__)
RECEIVED_FILES_FOLDER = 'downloads'
ACTIVITY_LOG_FILE = 'activity.log'

# Create required directories on startup
if not os.path.exists(RECEIVED_FILES_FOLDER):
    os.makedirs(RECEIVED_FILES_FOLDER)
if not os.path.exists(ACTIVITY_LOG_FILE):
    open(ACTIVITY_LOG_FILE, 'w').close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send')
def send_page():
    return render_template('send.html')


@app.route('/receive')
def receive_page():
    return render_template('receive.html')


@app.route('/api/start_receiver', methods=['POST'])
def api_start_receiver():
    success = app_functions.start_receiver()
    return jsonify({'status': 'listening' if success else 'already_running'})


@app.route('/api/stop_receiver', methods=['POST'])
def api_stop_receiver():
    success = app_functions.stop_receiver()
    return jsonify({'status': 'stopped' if success else 'not_running'})


@app.route('/api/receiver_status')
def api_receiver_status():
    status = 'listening' if app_functions.RECEIVER_PROCESS and app_functions.RECEIVER_PROCESS.poll() is None else 'not_running'
    return jsonify({'status': status})



@app.route('/api/send_files', methods=['POST'])
def api_send_files():
    ip = request.form.get('ip')
    files = request.files.getlist('files')
    print(f"Received files for IP: {ip}")
    print(f"Received files: {files}")
    # Save uploaded files temporarily
    temp_files = []
    for file in files:
        temp_path = os.path.join('temp_uploads', file.filename)
        file.save(temp_path)
        temp_files.append(temp_path)

    # **TEMPORARY CHANGE FOR TESTING:** Add placeholder file paths
    # temp_files = ['temp_uploads/LAB_practice.pdf', 'temp_uploads/LAB_practice - Copy.pdf']
    # print(f"File paths (for testing): {temp_files}")

    results = app_functions.send_files(ip, temp_files)

    # Cleanup temp files
    for f in temp_files:
        os.remove(f)
    return jsonify(results)


# @app.route('/api/send_files', methods=['POST'])
# def api_send_files():
#     ip = request.form.get('ip')
#     if not ip:
#         return jsonify([{'error': 'No IP provided'}]), 400
#
#     # The key must match what your frontend sends: 'files' (not 'files[]')
#     files = request.files.getlist('files')
#     print(f"Received files for IP: {ip}")
#     print(f"Number of files received: {len(files)}")
#     for idx, file in enumerate(files):
#         print(f"File {idx}: {file.filename} ({file.content_length} bytes)")
#
#     if not files or files[0].filename == '':
#         return jsonify([{'error': 'No files uploaded'}]), 400
#
#     # Create temp_uploads directory if it doesn't exist
#     if not os.path.exists('temp_uploads'):
#         os.makedirs('temp_uploads')
#
#     # Save uploaded files temporarily
#     temp_files = []
#     for file in files:
#         temp_path = os.path.join('temp_uploads', file.filename)
#         file.save(temp_path)
#         temp_files.append(temp_path)
#     print(f"Saved files to: {temp_files}")
#
#     results = []
#     # Iterate and send files one by one
#     for temp_file in temp_files:
#         try:
#             # Execute sender.py as a subprocess
#             process = subprocess.run(['python', 'sender.py', ip, temp_file], capture_output=True, text=True)
#             results.append({
#                 'file': os.path.basename(temp_file),
#                 'status': 'success' if process.returncode == 0 else 'error',
#                 'output': process.stdout.strip(),
#                 'error': process.stderr.strip()
#             })
#             print(f"Sent file: {temp_file}")
#         except Exception as e:
#             results.append({
#                 'file': os.path.basename(temp_file),
#                 'status': 'error',
#                 'error': str(e)
#             })
#             print(f"Error sending file {temp_file}: {e}")
#
#     # Cleanup temp files
#     for f in temp_files:
#         try:
#             os.remove(f)
#             print(f"Cleaned up: {f}")
#         except Exception as e:
#             print(f"Error cleaning up {f}: {e}")
#
#     return jsonify(results)




@app.route('/api/received_files')
def api_received_files():
    files = []
    if os.path.exists(RECEIVED_FILES_FOLDER):
        files = [{'name': f} for f in os.listdir(RECEIVED_FILES_FOLDER)
                 if os.path.isfile(os.path.join(RECEIVED_FILES_FOLDER, f))]
    return jsonify(files)


@app.route('/api/activity_log')
def api_activity_log():
    logs = []
    if os.path.exists(ACTIVITY_LOG_FILE):
        with open(ACTIVITY_LOG_FILE, 'r') as f:
            for line in f:
                match = re.match(r'\[(.*?)\]\s*(.*)', line.strip())
                if match:
                    logs.append({'time': match.group(1), 'msg': match.group(2)})
    return jsonify(logs)



@app.route('/api/clear_activity_log', methods=['POST'])
def api_clear_activity_log():
    open(ACTIVITY_LOG_FILE, 'w').close()
    return jsonify({'status': 'cleared'})


if __name__ == '__main__':
    if not os.path.exists('temp_uploads'):
        os.makedirs('temp_uploads')
    app.run(host='0.0.0.0', port=5000, debug=True)
