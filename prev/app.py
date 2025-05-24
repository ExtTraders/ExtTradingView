from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import json
import ccxt
import services.myBinance as myBinance
import services.myUpbit as myUpbit
#import myBybit
import keys.ende_key as ende_key
import keys.my_key as my_key
import line_alert

app = FastAPI()

# 암복호화 클래스 객체 생성
simpleEnDecrypt = myUpbit.SimpleEnDecrypt(ende_key.ende_key)

# Pydantic 모델 정의
class WebhookData(BaseModel):
    dist: str
    ticker: str
    type: str
    side: str
    price_money: float = None
    amt: float = None
    etc_num: float = None
    etc_str: str = None

@app.post("/webhook")
async def webhook(data: WebhookData):
    try:
        # 업비트 처리
        if data.dist == "upbit":
            Upbit_AccessKey = simpleEnDecrypt.decrypt(my_key.upbit_access)
            Upbit_ScretKey = simpleEnDecrypt.decrypt(my_key.upbit_secret)
            upbit = myUpbit.Upbit(Upbit_AccessKey, Upbit_ScretKey)

            if data.type == "market":
                if data.side == "buy":
                    balances = myUpbit.BuyCoinMarket(upbit, data.ticker, data.price_money)
                elif data.side == "sell":
                    balances = myUpbit.SellCoinMarket(upbit, data.ticker, data.amt)
            elif data.type == "limit":
                if data.side == "buy":
                    myUpbit.BuyCoinLimit(upbit, data.ticker, data.price_money, data.amt)
                elif data.side == "sell":
                    myUpbit.SellCoinLimit(upbit, data.ticker, data.price_money, data.amt)
            elif data.type == "cancel":
                myUpbit.CancelCoinOrder(upbit, data.ticker)

        # 바이낸스 처리
        elif data.dist == "binance":
            tmp = simpleEnDecrypt.encrypt(my_key.binance_access)
            Binance_AccessKey = simpleEnDecrypt.decrypt(tmp)
            tmp = simpleEnDecrypt.encrypt(my_key.binance_secret)
            Binance_ScretKey = simpleEnDecrypt.decrypt(tmp)
            binanceX = ccxt.binance({
                'apiKey': Binance_AccessKey,
                'secret': Binance_ScretKey,
                'enableRateLimit': True,
                'options': {'defaultType': 'future'}
            })
            
            # 바이낸스 모드 선택
            if(data.positionside == "hedge"):
                mode_status = binanceX.fapiprivate_get_positionside_dual()
                if(mode_status['dualSidePosition'] == False):
                    # 바이낸스에서 Hedge Mode 설정
                    binanceX.fapiprivate_post_positionside_dual({
                        "dualSidePosition": True  # Hedge Mode 설정
                    })
            elif(data.positionside == "oneway"):
                mode_status = binanceX.fapiprivate_get_positionside_dual()
                if(mode_status['dualSidePosition'] == True):
                    # 바이낸스에서 Hedge Mode 해제
                    binanceX.fapiprivate_post_positionside_dual({
                        "dualSidePosition": False  # Hedge Mode 해제
                    })
                    
            binanceX.load_markets()
            if data.type == "market":
                if data.side == "long":
                    response = binanceX.create_order(data.ticker, 'market', 'buy', data.amt)
                elif data.side == "short":
                    response = binanceX.create_order(data.ticker, 'market', 'sell', data.amt)
            elif data.type == "future":
                if data.side == "long":
                    
                    response = binanceX.set_leverage(4,symbol="XRP/USDT")
                    print(response)
                    response = binanceX.set_margin_mode(marginMode='cross', symbol="XRP/USDT")
                    print(response)
                    response = binanceX.create_order(data.ticker, type="MARKET", side='buy', amount=data.amt)
                    print(response)
                elif data.side == "short":
                    response = binanceX.create_order(data.ticker, 'market', 'sell', data.amt)
            elif data.type == "limit":
                if data.side == "long":
                    response = binanceX.create_order(data.ticker, 'limit', 'buy', data.amt, data.price_money)
                elif data.side == "short":
                    response = binanceX.create_order(data.ticker, 'limit', 'sell', data.amt, data.price_money)
            elif data.type == "cancel":
                response = binanceX.cancel_all_orders(data.ticker)
            elif data.type == "stop":
                response = myBinance.SetStopLoss(binanceX, data.ticker, data.etc_num, False)
                
            

        #바이비트 처리
        elif data.dist == "bybit":
            Bybit_AccessKey = simpleEnDecrypt.decrypt(my_key.bybit_access)
            Bybit_ScretKey = simpleEnDecrypt.decrypt(my_key.bybit_secret)
            bybitX = ccxt.bybit({
                'apiKey': Bybit_AccessKey,
                'secret': Bybit_ScretKey,
                'enableRateLimit': True,
                'options': {'defaultType': 'future'}
            })

            if data.type == "market":
                if data.etc_str == "open":
                    if data.side == "long":
                        response = bybitX.create_order(data.ticker, 'market', 'buy', data.amt, None, {'position_idx': 1})
                    elif data.side == "short":
                        response = bybitX.create_order(data.ticker, 'market', 'sell', data.amt, None, {'position_idx': 2})
                elif data.etc_str == "close":
                    if data.side == "long":
                        response = bybitX.create_order(data.ticker, 'market', 'buy', data.amt, None, {'position_idx': 1, 'reduce_only': True, 'close_on_trigger': True})
                    elif data.side == "short":
                        response = bybitX.create_order(data.ticker, 'market', 'sell', data.amt, None, {'position_idx': 2, 'reduce_only': True, 'close_on_trigger': True})
                        
            elif data.type == "limit":
                if data.etc_str == "open":
                    if data.side == "long":
                        response = bybitX.create_order(data.ticker, 'limit', 'buy', data.amt, data.price_money, {'position_idx': 1})
                    elif data.side == "short":
                        response = bybitX.create_order(data.ticker, 'limit', 'sell', data.amt, data.price_money, {'position_idx': 2})
                elif data.etc_str == "close":
                    if data.side == "long":
                        response = bybitX.create_order(data.ticker, 'limit', 'buy', data.amt, data.price_money, {'position_idx': 1, 'reduce_only': True, 'close_on_trigger': True})
                    elif data.side == "short":
                        response = bybitX.create_order(data.ticker, 'limit', 'sell', data.amt, data.price_money, {'position_idx': 2, 'reduce_only': True, 'close_on_trigger': True})
            elif data.type == "cancel":
                response = myBybit.CancelAllOrder(bybitX, data.ticker)
            elif data.type == "stop":
                response = myBybit.SetStopLoss(bybitX, data.ticker, data.etc_num, False)

        else:
            raise HTTPException(status_code=400, detail="Unsupported 'dist' value")

        # 성공 메시지 전송
        line_alert.SendMessage(f"MsgTest: {data.dict()}")
        return {"success": True, "message": "Webhook processed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))