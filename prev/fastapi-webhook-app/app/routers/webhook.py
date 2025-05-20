from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from app.services import trading
from app.utils import encryption, alert

router = APIRouter()

class WebhookData(BaseModel):
    dist: str
    ticker: str
    type: str
    side: str
    price_money: float = None
    amt: float = None
    etc_num: float = None
    etc_str: str = None

@router.post("/webhook")
async def handle_webhook(data: WebhookData):
    try:
        if data.dist == "upbit":
            return trading.handle_upbit(data)
        elif data.dist == "binance":
            return trading.handle_binance(data)
        elif data.dist == "bybit":
            return trading.handle_bybit(data)
        else:
            raise HTTPException(status_code=400, detail="Unsupported exchange")
    except Exception as e:
        alert.send_message(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")