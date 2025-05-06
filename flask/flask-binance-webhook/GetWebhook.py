from flask import Flask, request, jsonify
import json
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data and data.get('dist') == 'binance':
        # Convert the data to a JSON string for the subprocess call
        json_data = json.dumps(data)
        
        # Call the GetWebhook.py script with the JSON data as an argument
        try:
            result = subprocess.run(['python', 'GetWebhook.py', json_data], capture_output=True, text=True)
            return jsonify({'status': 'success', 'output': result.stdout}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'ignored', 'message': 'Invalid or unsupported request'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)