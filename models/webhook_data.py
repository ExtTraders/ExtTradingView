from pydantic import BaseModel

class WebhookData(BaseModel):
    dist: str
    order_type: str
    symbol: str
    type: str
    side: str
    price_money: float = None
    amount: float = None
    etc_num: float = None
    etc_str: str = None