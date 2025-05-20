from flask import Flask, request, jsonify
import json
import ccxt
import keys.my_key as my_key
import keys.ende_key as ende_key
import services.myBinance as myBinance

app = Flask(__name__)

# 암복호화 클래스 객체 생성
simpleEnDecrypt = myBinance.SimpleEnDecrypt(ende_key.ende_key)

@app.route('/webhook', methods=['POST'])
def webhook():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)