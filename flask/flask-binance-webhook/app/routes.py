from flask import Blueprint, request, jsonify
import json
import subprocess

bp = Blueprint('webhook', __name__)

@bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data and data.get('dist') == 'binance':
        try:
            # Convert the data to a JSON string for the subprocess call
            json_data = json.dumps(data)
            # Call the GetWebhook.py script with the JSON data as an argument
            result = subprocess.run(['python', 'GetWebhook.py', json_data], capture_output=True, text=True)
            return jsonify({'status': 'success', 'output': result.stdout}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'error', 'message': 'Invalid data or dist not binance'}), 400