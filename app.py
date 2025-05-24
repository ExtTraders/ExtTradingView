from fastapi import FastAPI, HTTPException
from models.webhook_data import WebhookData
from models.encrypt_data import EncryptData
from services.binance_service import BinanceService
from services.upbit_service import UpbitService
from services.bybit_service import BybitService
from services.showEncryptAccessKey import showEncryptAccessKey
from utils.alert import send_alert
import my_key
import ende_key
import logging
from datetime import datetime

app = FastAPI()

@app.post("/webhook")
async def webhook(data: WebhookData):
    try:
        if data.exchange == "binance":
            service = BinanceService(my_key.binance_access, my_key.binance_secret, ende_key.ende_key)
        elif data.exchange == "upbit":
            service = UpbitService(my_key.upbit_access, my_key.upbit_secret, ende_key.ende_key)
        elif data.exchange == "bybit":
            service = BybitService(my_key.bybit_access, my_key.bybit_secret, ende_key.ende_key)
        elif data.exchange == "tbybit":
            service = BybitService(my_key.bybit_test_access, my_key.bybit_test_secret, ende_key.ende_key)
        else:
            raise HTTPException(status_code=400, detail="Unsupported 'exchange' value")

        # 주문 처리
        response = service.place_order(data)
        send_alert(f"Order placed: {response}")
        return {"success": True, "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/msgtest")
async def msgtest(request: dict):

    # 로그 파일 설정
    logging.basicConfig(
        filename="./msgtest.log",
        level=logging.INFO,
        format="%(asctime)s %(message)s"
    )

    # 메시지 출력
    print("Received message:", request)

    # 로그 파일에 기록
    logging.info(f"Received message: {request}")

    return {"success": True, "message": "Message received and logged."}
    
@app.post("/encrypt")
async def encrypt(data: EncryptData):
    try:
        service = showEncryptAccessKey()
        response = service.encryptCode(data.access_key, data.secret_key, ende_key.ende_key)
        return {
            "success": True,
            "response": {
                "encrypt_access_key": response[0],
                "encrypt_secret_key": response[1]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
