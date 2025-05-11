# FastAPI Webhook Application

This project is a FastAPI application designed to handle webhook requests for trading platforms such as Upbit, Binance, and Bybit. It processes incoming data, executes trades, and manages alerts.

## Project Structure

```
fastapi-webhook-app
├── app
│   ├── main.py               # Entry point of the FastAPI application
│   ├── routers
│   │   └── webhook.py        # Defines the webhook endpoint
│   ├── services
│   │   └── trading.py        # Logic for interacting with trading platforms
│   ├── utils
│   │   ├── encryption.py      # Utility functions for encrypting/decrypting API keys
│   │   └── alert.py           # Functions for sending alerts or messages
│   └── __init__.py           # Marks the app directory as a Python package
├── requirements.txt           # Lists dependencies for the FastAPI application
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-webhook-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Usage

- The application listens for webhook requests at the `/webhook` endpoint.
- Incoming requests should contain the necessary data for executing trades on the specified platform.
- The application will process the requests and execute trades accordingly.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.