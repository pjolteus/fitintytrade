import hmac
import hashlib
import time
import requests
import logging
from urllib.parse import urlencode

# Bybit API base (for spot or derivatives, adjust if needed)
BASE_URL = "https://api.bybit.com"  # Mainnet for perpetual futures
API_VERSION = "v2"  # You can upgrade to v5 with different endpoints

class BybitConnector:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, params: dict):
        sorted_params = urlencode(sorted(params.items()))
        return hmac.new(
            self.api_secret.encode("utf-8"),
            sorted_params.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _send_request(self, method: str, endpoint: str, params: dict):
        url = f"{BASE_URL}/{API_VERSION}/{endpoint}"
        params["api_key"] = self.api_key
        params["timestamp"] = self._get_timestamp()
        params["sign"] = self._sign(params)

        try:
            if method == "GET":
                response = requests.get(url, params=params)
            elif method == "POST":
                response = requests.post(url, data=params)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Bybit API error: {e}")
            return None

    def get_price(self, symbol="BTCUSDT"):
        try:
            url = f"{BASE_URL}/v2/public/tickers"
            response = requests.get(url, params={"symbol": symbol})
            response.raise_for_status()
            data = response.json()
            return float(data["result"][0]["last_price"])
        except Exception as e:
            logging.error(f"Failed to get price from Bybit: {e}")
            return None

    def place_order(self, symbol, side, qty, order_type="Market", price=None):
        endpoint = "private/order/create"
        params = {
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "qty": qty,
            "time_in_force": "GoodTillCancel",
        }
        if order_type == "Limit" and price:
            params["price"] = price

        return self._send_request("POST", endpoint, params)

    def get_positions(self):
        endpoint = "private/position/list"
        params = {"symbol": "BTCUSDT"}
        return self._send_request("GET", endpoint, params)
