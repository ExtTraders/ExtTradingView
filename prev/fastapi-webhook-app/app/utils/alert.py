from fastapi import HTTPException
import requests

def send_message(message: str):
    # Here you can implement the logic to send alerts, e.g., via a messaging service
    # For example, sending a message to a Slack channel or a Discord webhook
    webhook_url = "YOUR_WEBHOOK_URL"  # Replace with your actual webhook URL
    payload = {"text": message}
    
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to send alert")