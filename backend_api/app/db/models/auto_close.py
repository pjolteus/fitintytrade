from celery import shared_task
import logging
from connectors import alpaca, oanda, fxcm, ibr

BROKERS = {
    "alpaca": alpaca,
    "oanda": oanda,
    "fxcm": fxcm,
    "ibr": ibr
}

@shared_task
def auto_close_positions_task():
    logging.info("Running auto-close for open positions")
    for name, broker in BROKERS.items():
        try:
            _close_all_positions(broker, name)
        except Exception as e:
            logging.error(f"Auto-close failed for {name}: {e}")

def _close_all_positions(broker, name):
    positions = broker.get_all_positions() if hasattr(broker, "get_all_positions") else []
    for pos in positions:
        symbol = pos.get("symbol")
        qty = abs(pos.get("qty", 0))
        side = "sell" if pos.get("qty", 0) > 0 else "buy"
        if qty > 0:
            logging.info(f"[{name}] Closing {symbol} x{qty}")
            broker.place_order(symbol, qty, side)
