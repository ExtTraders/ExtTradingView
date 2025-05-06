# Flask Binance Webhook

This project is a Flask application that listens for incoming webhook requests specifically for trading on Binance. It processes the requests and executes trading commands based on the provided parameters.

## Project Structure

```
flask-binance-webhook
├── app
│   ├── __init__.py          # Initializes the Flask application and sets up configurations and routes.
│   ├── routes.py            # Defines the routes for the Flask application.
│   └── utils
│       └── execute_webhook.py # Contains logic to execute the webhook functionality.
├── GetWebhook.py            # Main logic for handling webhook requests related to trading on Binance.
├── requirements.txt         # Lists the dependencies required for the project.
└── README.md                # Documentation for the project.
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-binance-webhook
   ```

2. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the Flask application:**
   ```
   python -m flask run
   ```

   Make sure to set the `FLASK_APP` environment variable to `app`.

## Usage

To trigger the webhook functionality, send a POST request to the `/webhook` endpoint with the following JSON structure:

```json
{
    "dist": "binance",
    "ticker": "BTC/USDT",
    "type": "market",
    "side": "long",
    "price_money": 50000,
    "amt": 0.1,
    "etc_num": 0.2,
    "etc_str": ""
}
```

### Example

You can use tools like `curl` or Postman to send a request:

```bash
curl -X POST http://localhost:5000/webhook -H "Content-Type: application/json" -d '{
    "dist": "binance",
    "ticker": "BTC/USDT",
    "type": "market",
    "side": "long",
    "price_money": 50000,
    "amt": 0.1,
    "etc_num": 0.2,
    "etc_str": ""
}'
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.