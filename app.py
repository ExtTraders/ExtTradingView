from fastapi import FastAPI, HTTPException
from models.webhook_data import WebhookData
from services.binance_service import BinanceService
from services.upbit_service import UpbitService
from utils.alert import send_alert
import my_key
import ende_key

app = FastAPI()

@app.post("/webhook")
async def webhook(data: WebhookData):
    try:
        if data.dist == "binance":
            service = BinanceService(my_key.binance_access, my_key.binance_secret, ende_key.ende_key)
        elif data.dist == "upbit":
            service = UpbitService(my_key.upbit_access, my_key.upbit_secret, ende_key.ende_key)
        else:
            raise HTTPException(status_code=400, detail="Unsupported 'dist' value")

        # 주문 처리
        response = service.place_order(data)
        send_alert(f"Order placed: {response}")
        return {"success": True, "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))