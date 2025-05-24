import pytest
from fastapi.testclient import TestClient
from app import app
from services.binance_service import BinanceService
from services.bybit_service import BybitService
from services.showEncryptAccessKey import showEncryptAccessKey
from utils.encryption import SimpleEnDecrypt


client = TestClient(app)

def test_msgtest():
    payload = {"msg": "hello"}
    response = client.post("/msgtest", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "Message received" in response.json()["message"]

def test_webhook_binance(monkeypatch):
    monkeypatch.setattr("services.binance_service.BinanceService", BinanceService)
    monkeypatch.setattr("utils.alert.send_alert", lambda msg: None)
    payload = {
        "exchange": "binance",
        "open_order":"future",
        "symbol":"XRP/USDT",
        "type":"market",
        "side":"buy",
        "amount":5
    }
    response = client.post("/webhook", json=payload)
    print(response.json())
    assert response.status_code == 200
    # assert response.json()["success"] is True
    # assert response.json()["response"]["order_id"] == "123"

def test_webhook_bybit_testnet(monkeypatch):
    payload = {
        "dist": "bybit",
        "open_order":"future",
        "symbol":"XRP/USDT",
        "type":"market",
        "side":"buy",
        "amount":5
    }
    response = client.post("/webhook", json=payload)
    print(response.json())
    assert response.status_code == 200

def test_webhook_bybit(monkeypatch):
    payload = {
        "dist": "bybit",
        "open_order":"future",
        "symbol":"XRP/USDT",
        "type":"market",
        "side":"buy",
        "amount":5
    }
    response = client.post("/webhook", json=payload)
    print(response.json())
    assert response.status_code == 200


def test_webhook_invalid_dist():
    payload = {
        "dist": "unknown",
        "access_key": "a",
        "secret_key": "b",
        "symbol": "BTCUSDT",
        "side": "buy",
        "price": 10000,
        "quantity": 0.01,
        "open_order": "market"
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 400
    assert "Unsupported" in response.json()["detail"]

def test_webhook_service_exception(monkeypatch):
    class DummyService:
        def __init__(self, a, b, c): pass
        def place_order(self, data): raise Exception("fail!")
    monkeypatch.setattr("services.binance_service.BinanceService", DummyService)
    monkeypatch.setattr("utils.alert.send_alert", lambda msg: None)
    payload = {
        "dist": "binance",
        "symbol": "BTCUSDT",
        "side": "buy",
        "price": 10000,
        "quantity": 0.01,
        "open_order": "market"
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 500
    assert "fail!" in response.json()["detail"]

def test_encrypt_result(monkeypatch):
    #monkeypatch.setattr("services.showEncryptAccessKey.showEncryptAccessKey", showEncryptAccessKey)
    payload = {
        "access_key": "7qoG4DivEhy6AW7esa",
        "secret_key": "L6amg4o32JIBpSCFu4tkoJzrUzlTF4oRiseQ",
    }
    response = client.post("/encrypt", json=payload)
    print(response.json())
    assert response.status_code == 500

    