from utils.encryption import SimpleEnDecrypt
import ccxt

class BaseService:
    def __init__(self, access_key, secret_key, encryption_key):
        self.encryption = SimpleEnDecrypt(encryption_key)
        self.access_key = self.encryption.decrypt(access_key)
        self.secret_key = self.encryption.decrypt(secret_key)

    def create_exchange(self, exchange_name, options=None):
        if exchange_name == "binance":
            return ccxt.binance({
                'apiKey': self.access_key,
                'secret': self.secret_key,
                'enableRateLimit': True,
                'options': options or {}
            })
        elif exchange_name == "upbit":
            # Upbit 객체 생성 로직
            pass
        elif exchange_name == "bybit":
            return ccxt.bybit({
                'apiKey': self.access_key,
                'secret': self.secret_key,
                'enableRateLimit': True,
                'options': options or {}
            })
        else:
            raise ValueError(f"Unsupported exchange: {exchange_name}")