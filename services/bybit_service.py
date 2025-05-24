from services.base_service import BaseService
import ccxt

class BybitService(BaseService):
    def __init__(self, access_key, secret_key, encryption_key):
        super().__init__(access_key, secret_key, encryption_key)
        self.exchange = self.create_exchange("bybit", {'defaultType': 'future'})

    def set_leverage(self, leverage: int, symbol: str):
        # 바이낸스 선물 레버리지 설정
        return self.exchange.private_post_position_lev({
            "symbol": self.exchange.market_id(symbol),
            "leverage": leverage
        })
        
    def place_order(self, data):
        params = {}
        if hasattr(data, "etc_str") and data.etc_str:
            if data.etc_str == "open":
                params['position_idx'] = 1 if data.side == "long" else 2
            elif data.etc_str == "close":
                params['position_idx'] = 1 if data.side == "long" else 2
                params['reduce_only'] = True
                params['close_on_trigger'] = True
                
        if hasattr(data, "leverage") and data.leverage:
            self.set_leverage(data.leverage, data.symbol)

        if data.type == "market":
            return self.exchange.create_order(data.ticker, 'market', data.side, data.amt, None, params)
        elif data.type == "limit":
            return self.exchange.create_order(data.ticker, 'limit', data.side, data.amt, data.price_money, params)
        elif data.type == "cancel":
            # Cancel all orders (구현 필요)
            pass
        elif data.type == "stop":
            # Stop loss (구현 필요)
            pass
        else:
            raise ValueError(f"Unsupported order type: {data.type}")