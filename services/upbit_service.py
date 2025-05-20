from services.base_service import BaseService
import services.myUpbit as myUpbit

#########
# 업비트 서비스 클래스
# 미개발
#########
class UpbitService(BaseService):
    def __init__(self, access_key, secret_key, encryption_key):
        super().__init__(access_key, secret_key, encryption_key)
        self.exchange = myUpbit.Upbit(self.access_key, self.secret_key)

    def place_order(self, data):
        if data.type == "market":
            if data.side == "buy":
                return myUpbit.BuyCoinMarket(self.exchange, data.ticker, data.price_money)
            elif data.side == "sell":
                return myUpbit.SellCoinMarket(self.exchange, data.ticker, data.amt)
        elif data.type == "limit":
            if data.side == "buy":
                return myUpbit.BuyCoinLimit(self.exchange, data.ticker, data.price_money, data.amount)
            elif data.side == "sell":
                return myUpbit.SellCoinLimit(self.exchange, data.ticker, data.price_money, data.amount)
        elif data.type == "cancel":
            return myUpbit.CancelCoinOrder(self.exchange, data.ticker)
        else:
            raise ValueError(f"Unsupported order type: {data.type}")