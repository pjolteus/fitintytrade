import os
import logging
import fxcmpy
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

# ⚙️ Configuration
FXCM_MODE = os.getenv("FXCM_MODE", "demo")  # demo or live
FXCM_TOKEN = os.getenv("FXCM_API_TOKEN")
FXCM_SERVER = "demo" if FXCM_MODE == "demo" else "real"

# 🔌 Establish connection
_connection = None

def get_connection():
    global _connection
    if _connection is None or not _connection.is_connected():
        _connection = fxcmpy.fxcmpy(access_token=FXCM_TOKEN, log_level='error', server=FXCM_SERVER)
        logging.info(f"Connected to FXCM ({FXCM_MODE})")
    return _connection


# 🔁 Retry wrapper
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def place_fxcm_order(instrument: str, units: int, side: str, stop_loss=None, take_profit=None, trailing_stop=None):
    """
    Places a market order with FXCM with optional SL/TP/Trailing.
    """
    con = get_connection()

    order_args = {
        'symbol': instrument,
        'is_buy': side.lower() == 'buy',
        'amount': abs(units),
        'order_type': 'AtMarket',
        'time_in_force': 'GTC'
    }

    if stop_loss:
        order_args['stop'] = stop_loss
    if take_profit:
        order_args['limit'] = take_profit
    if trailing_stop:
        order_args['trailing_step'] = trailing_stop

    logging.info(f"Placing FXCM order: {order_args}")
    order_id = con.open_trade(**order_args)

    if not order_id:
        raise Exception("FXCM order failed or not returned")

    return {"order_id": str(order_id), "status": "submitted"}


def get_order_status(order_id: str):
    con = get_connection()
    trades = con.get_open_trade_ids()
    if int(order_id) not in trades:
        return {"order_id": order_id, "status": "closed"}
    trade = con.get_open_trade(int(order_id))
    return {"order_id": order_id, "status": "open", "details": trade.get_trade_data()}


def cancel_order(order_id: str):
    con = get_connection()
    try:
        con.close_trade(trade_id=int(order_id))
        return {"order_id": order_id, "status": "cancelled"}
    except Exception as e:
        logging.error(f"FXCM cancel failed: {e}")
        raise


def get_position(instrument: str):
    con = get_connection()
    positions = con.get_open_positions()
    if positions.empty:
        return None
    filtered = positions[positions['currency'] == instrument]
    if filtered.empty:
        return None
    return filtered.to_dict(orient="records")[0]

def get_all_positions():
    pos = conn.get_open_positions()
    return [
        {
            "symbol": row["currency"],
            "qty": abs(float(row["amount"]))
        } for _, row in pos.iterrows()
    ]

