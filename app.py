# app.py
from flask import Flask, render_template, request, jsonify
import app_functions

app = Flask(__name__)

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
    started = app_functions.start_receiver()
    return jsonify({'status': 'listening' if started else 'already_listening'})

@app.route('/api/stop_receiver', methods=['POST'])
def api_stop_receiver():
    stopped = app_functions.stop_receiver()
    return jsonify({'status': 'stopped' if stopped else 'not_running'})

@app.route('/api/send_files', methods=['POST'])
def api_send_files():
    ip = request.form.get('ip')
    files = request.form.getlist('files[]')
    results = app_functions.send_files(ip, files)
    return jsonify(results)

@app.route('/api/received_files')
def received_files():
    # Example: return [{'name': 'example.txt'}, ...]
    # You should implement logic to read received files from your storage
    return jsonify([{'name': f} for f in os.listdir(RECEIVED_FILES_FOLDER)])

@app.route('/api/clear_activity_log', methods=['POST'])
def clear_activity_log():
    # Example: If you store log in a file
    with open('activity.log', 'w') as f:
        f.write('')
    # Or if you use a global list, just clear it
    # activity_log.clear()
    return jsonify({"status": "cleared"})


if __name__ == '__main__':
    app.run(debug=True)
