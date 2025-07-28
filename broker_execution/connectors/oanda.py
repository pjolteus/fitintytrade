import os
import requests
import logging
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

# Configuration
OANDA_MODE = os.getenv("OANDA_MODE", "sandbox")  # sandbox or live
OANDA_API_KEY = os.getenv("OANDA_API_KEY")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")

OANDA_BASE_URL = (
    "https://api-fxpractice.oanda.com/v3" if OANDA_MODE == "sandbox"
    else "https://api-fxtrade.oanda.com/v3"
)

HEADERS = {
    "Authorization": f"Bearer {OANDA_API_KEY}",
    "Content-Type": "application/json"
}

# Retry wrapper
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def place_forex_order(instrument: str, units: int, side: str, stop_loss=None, take_profit=None, trailing_stop=None):
    """
    Places a market order on OANDA with optional stop-loss, take-profit, and trailing stop.
    """
    url = f"{OANDA_BASE_URL}/accounts/{OANDA_ACCOUNT_ID}/orders"

    order_data = {
        "order": {
            "type": "MARKET",
            "instrument": instrument,
            "units": str(units if side == "buy" else -units),
            "timeInForce": "FOK",
            "positionFill": "DEFAULT"
        }
    }

    # Add stop-loss, take-profit, trailing stop
    stop_loss_fields = {}
    if stop_loss:
        stop_loss_fields["stopLossOnFill"] = {"price": str(stop_loss)}
    if take_profit:
        stop_loss_fields["takeProfitOnFill"] = {"price": str(take_profit)}
    if trailing_stop:
        stop_loss_fields["trailingStopLossOnFill"] = {"distance": str(trailing_stop)}

    order_data["order"].update(stop_loss_fields)

    response = requests.post(url, json=order_data, headers=HEADERS)

    if response.status_code != 201:
        logging.error(f"OANDA order failed: {response.text}")
        raise Exception(f"Order error: {response.text}")

    return response.json()


def get_order_status(order_id: str):
    url = f"{OANDA_BASE_URL}/accounts/{OANDA_ACCOUNT_ID}/orders/{order_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        logging.error(f"Failed to get OANDA order status: {response.text}")
        raise Exception(f"Status error: {response.text}")
    return response.json()


def cancel_order(order_id: str):
    url = f"{OANDA_BASE_URL}/accounts/{OANDA_ACCOUNT_ID}/orders/{order_id}/cancel"
    response = requests.put(url, headers=HEADERS)
    if response.status_code != 200:
        logging.warning(f"OANDA cancel failed: {response.text}")
        raise Exception(f"Cancel error: {response.text}")
    return {"status": "cancelled", "order_id": order_id}


def get_position(instrument: str):
    url = f"{OANDA_BASE_URL}/accounts/{OANDA_ACCOUNT_ID}/positions/{instrument}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 404:
        return None
    elif response.status_code != 200:
        raise Exception(f"Position error: {response.text}")
    return response.json()

def get_all_positions():
    url = f"{OANDA_BASE_URL}/accounts/{OANDA_ACCOUNT_ID}/openPositions"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"OANDA positions error: {response.text}")
    positions = response.json().get("positions", [])
    return [
        {
            "symbol": p["instrument"],
            "qty": float(p["long"]["units"]) if float(p["long"]["units"]) != 0 else float(p["short"]["units"])
        } for p in positions
    ]


