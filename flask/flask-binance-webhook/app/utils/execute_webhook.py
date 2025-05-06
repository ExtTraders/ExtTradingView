from flask import request, jsonify
import json
import subprocess

def execute_binance_webhook(data):
    try:
        # Convert the data dictionary to a JSON string
        json_data = json.dumps(data)
        
        # Call the GetWebhook.py script with the JSON data as an argument
        result = subprocess.run(['python', 'GetWebhook.py', json_data], capture_output=True, text=True)
        
        # Check if the script executed successfully
        if result.returncode == 0:
            return jsonify({"status": "success", "output": result.stdout}), 200
        else:
            return jsonify({"status": "error", "message": result.stderr}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500