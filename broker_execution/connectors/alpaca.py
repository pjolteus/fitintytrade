import os
import requests
import logging
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

# Config: Sandbox or Live
ALPACA_MODE = os.getenv("ALPACA_MODE", "sandbox")
ALPACA_BASE_URL = "https://paper-api.alpaca.markets" if ALPACA_MODE == "sandbox" else "https://api.alpaca.markets"
HEADERS = {
    "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
    "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY")
}

# Retry wrapper
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def place_order(symbol: str, qty: int, side: str, stop_loss=None, take_profit=None, trailing_stop=None):
    """
    Place a market order with optional stop-loss, take-profit, and trailing stop.
    """
    url = f"{ALPACA_BASE_URL}/v2/orders"
    order_data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": "market",
        "time_in_force": "gtc"
    }

    # Advanced options
    if stop_loss or take_profit or trailing_stop:
        order_data["order_class"] = "bracket"
        order_data["stop_loss"] = {}
        order_data["take_profit"] = {}

        if stop_loss:
            order_data["stop_loss"]["stop_price"] = stop_loss
        if trailing_stop:
            order_data["stop_loss"]["trail_price"] = trailing_stop

        if take_profit:
            order_data["take_profit"]["limit_price"] = take_profit

    logging.info(f"Placing order: {order_data}")
    response = requests.post(url, json=order_data, headers=HEADERS)

    if response.status_code != 200:
        logging.error(f"Order failed: {response.text}")
        raise Exception(f"Order error: {response.text}")

    return response.json()


def get_order_status(order_id: str):
    url = f"{ALPACA_BASE_URL}/v2/orders/{order_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        logging.error(f"Failed to fetch order status: {response.text}")
        raise Exception(f"Status error: {response.text}")
    return response.json()


def cancel_order(order_id: str):
    url = f"{ALPACA_BASE_URL}/v2/orders/{order_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code != 204:
        logging.warning(f"Cancel failed: {response.text}")
        raise Exception(f"Cancel error: {response.text}")
    return {"status": "cancelled", "order_id": order_id}


def get_position(symbol: str):
    url = f"{ALPACA_BASE_URL}/v2/positions/{symbol}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 404:
        return None
    elif response.status_code != 200:
        raise Exception(f"Position error: {response.text}")
    return response.json()

def get_all_positions():
    url = f"{ALPACA_BASE_URL}/v2/positions"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to get positions: {response.text}")
    return response.json()


