import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode

BINANCE_SPOT_BASE_URL = "https://api.binance.com"
BINANCE_FUTURES_BASE_URL = "https://fapi.binance.com"

class BinanceConnector:
    def __init__(self, api_key: str, api_secret: str, use_futures: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = BINANCE_FUTURES_BASE_URL if use_futures else BINANCE_SPOT_BASE_URL

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, params: dict):
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _send_signed_request(self, method: str, endpoint: str, params: dict):
        headers = {"X-MBX-APIKEY": self.api_key}
        params["timestamp"] = self._get_timestamp()
        params["signature"] = self._sign(params)
        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, params=params)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Binance API Error: {e}")
            return None

    def _send_public_request(self, endpoint: str, params: dict = {}):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Public Binance API Error: {e}")
            return None

    def get_price(self, symbol: str = "BTCUSDT"):
        data = self._send_public_request("/fapi/v1/ticker/price", {"symbol": symbol}) if "fapi" in self.base_url else self._send_public_request("/api/v3/ticker/price", {"symbol": symbol})
        try:
            return float(data["price"])
        except:
            return None

    def place_order(self, symbol: str, side: str, quantity: float, order_type: str = "MARKET", price: float = None):
        endpoint = "/fapi/v1/order" if "fapi" in self.base_url else "/api/v3/order"
        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity
        }

        if order_type.upper() == "LIMIT" and price:
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._send_signed_request("POST", endpoint, params)

    def get_positions(self):
        if "fapi" not in self.base_url:
            logging.warning("Position info only supported in futures mode.")
            return None

        endpoint = "/fapi/v2/positionRisk"
        return self._send_signed_request("GET", endpoint, {})
