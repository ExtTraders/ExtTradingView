from fastapi import APIRouter, HTTPException
import ccxt
import json
from app.utils.encryption import SimpleEnDecrypt
from app.utils.alert import SendMessage

router = APIRouter()

@router.post("/webhook")
async def webhook(data: dict):
    try:
        # Assuming 'data' is already a dictionary from the request body
        if 'dist' not in data:
            raise HTTPException(status_code=400, detail="Missing 'dist' field in data")

        if data['dist'] == "upbit":
            return await handle_upbit(data)
        elif data['dist'] == "binance":
            return await handle_binance(data)
        elif data['dist'] == "bybit":
            return await handle_bybit(data)
        else:
            raise HTTPException(status_code=400, detail="Unsupported exchange")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def handle_upbit(data):
    # Logic for Upbit trading
    # Decrypt keys and interact with Upbit API
    pass

async def handle_binance(data):
    try:
        # Parse incoming JSON data
        data = request.get_json()
        
        print("test")

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        print("test")
        print(data['dist'])
        # Process Binance-specific logic
        if data['dist'] == 'binance':
            Binance_AccessKey = simpleEnDecrypt.decrypt(my_key.binance_access)
            print(Binance_AccessKey)
            Binance_ScretKey = simpleEnDecrypt.decrypt(my_key.binance_secret)
            print(Binance_ScretKey)
            # Create Binance object
            binanceX = ccxt.binance(config={
                'apiKey': Binance_AccessKey,
                'secret': Binance_ScretKey,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future'
                }
            })

            # Handle different types of orders
            if data['type'] == "market":
                if data['side'] == "long":
                    response = binanceX.create_order(data['ticker'], 'market', 'buy', data['amt'])
                elif data['side'] == "short":
                    response = binanceX.create_order(data['ticker'], 'market', 'sell', data['amt'])

            elif data['type'] == "limit":
                if data['side'] == "long":
                    response = binanceX.create_order(data['ticker'], 'limit', 'buy', data['amt'], data['price_money'])
                elif data['side'] == "short":
                    response = binanceX.create_order(data['ticker'], 'limit', 'sell', data['amt'], data['price_money'])

            elif data['type'] == 'cancel':
                response = binanceX.cancel_all_orders(data['ticker'])

            elif data['type'] == 'stop':
                response = myBinance.SetStopLoss(binanceX, data['ticker'], data['etc_num'], False)

            else:
                return jsonify({"error": "Invalid order type"}), 400

            return jsonify({"success": True, "response": response}), 200

        else:
            return jsonify({"error": "Unsupported 'dist' value"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

async def handle_bybit(data):
    # Logic for Bybit trading
    # Decrypt keys and interact with Bybit API
    pass

def create_order(exchange, ticker, order_type, side, amount, price=None, params=None):
    if order_type == 'market':
        return exchange.create_order(ticker, 'market', side, amount, None, params)
    elif order_type == 'limit':
        return exchange.create_order(ticker, 'limit', side, amount, price, params)
    else:
        raise ValueError("Invalid order type")