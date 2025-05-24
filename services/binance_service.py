from services.base_service import BaseService

class BinanceService(BaseService):
    def __init__(self, access_key, secret_key, encryption_key):
        super().__init__(access_key, secret_key, encryption_key)        

    def set_leverage(self, leverage: int, symbol: str):
        # 바이낸스 선물 레버리지 설정
        return self.exchange.fapiPrivate_post_leverage({
            "symbol": self.exchange.market_id(symbol),
            "leverage": leverage
        })

    def set_margin_mode(self, marginMode: str, symbol: str):
        # 바이낸스 선물 마진모드 설정
        return self.exchange.fapiPrivate_post_marginType({
            "symbol": self.exchange.market_id(symbol),
            "marginType": marginMode.upper()
        })
        
    def set_position_side(self, positionside: str):
        # positionside: "hedge" 또는 "oneway"
        mode_status = self.exchange.fapiprivate_get_positionside_dual()
        if positionside == "hedge" and not mode_status['dualSidePosition']:
            self.exchange.fapiprivate_post_positionside_dual({"dualSidePosition": True})
        elif positionside == "oneway" and mode_status['dualSidePosition']:
            self.exchange.fapiprivate_post_positionside_dual({"dualSidePosition": False})
                
    def place_order(self, data):
        if data.order_type == "spot":
            self.exchange = self.create_exchange("binance", {'defaultType': 'spot'})
        elif data.order_type == "future":
            self.exchange = self.create_exchange("binance", {'defaultType': 'future'})
        else:
            raise ValueError(f"Unsupported order type: {data.order_type}")

        if hasattr(data, "positionside") and data.positionside:
            self.set_position_side(data.positionside)
        if hasattr(data, "leverage") and data.leverage:
            self.set_leverage(data.leverage, data.symbol)
        if hasattr(data, "marginMode") and data.marginMode:
            self.set_margin_mode(data.marginMode, data.symbol)
        
        return self.exchange.create_order(data.symbol, data.type, data.side, data.amount)
        