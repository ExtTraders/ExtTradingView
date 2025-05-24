from pydantic import BaseMode

'''
TVM:{
    "exchange":"bybit",
    "account":"Reverse",
    "symbol":"ETH/USDT",
    "type":"market",
    "side":"buy",
    "bal_pct":' + tostring(truncate(longQty, 3)*10) + ',
    "open_order":"cancel",
    "leverage":10,
    "token":""}:MVT

{
  "exchange":"binance",
  "account":"Reverse",
  "symbol":"AVAX/USDT",
  "type":"market",
  "side":"buy",
  "bal_pct": 12.3,
  "open_order":"future",
  "leverage":10,
  "token":"",
  "amount": 5
}
'''
class WebhookData(BaseModel):
    exchange: str
    account: str = None
    symbol: str
    type: str
    side: str
    open_order: str
    leverage: int = None
    token: str = None
    price_money: float = None
    amount: float = None
    etc_num: float = None
    etc_str: str = None
    positionside: str = None
    marginMode: str = None