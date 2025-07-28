import logging
import time
import os
from celery import shared_task
from connectors import alpaca, oanda, ibr, fxcm
from db.connection import SessionLocal
from db.models.prediction import Prediction, PredictionFeedback
from utils.alerts import send_alert  # ⬅️ Slack/email via webhook

# Broker map
BROKER_MAP = {
    "alpaca": alpaca,
    "oanda": oanda,
    "ibr": ibr,
    "fxcm": fxcm
}

@shared_task(bind=True, name="trailing_take_profit_task")
def trailing_take_profit_task(self, symbol, qty, broker_name, side, order_id, trigger_pct):
    broker = BROKER_MAP[broker_name]
    entry = broker.get_position(symbol)
    if not entry:
        msg = f"[{symbol}] No position found. Aborting trailing TP."
        logging.warning(msg)
        send_alert(msg)
        return

    try:
        entry_price = float(entry["avg_price"])
    except (KeyError, ValueError, TypeError):
        logging.error(f"[{symbol}] Invalid entry price: {entry}")
        return

    best_price = entry_price
    threshold = trigger_pct / 100

    logging.info(f"[{symbol}] Trailing TP monitor started at entry: {entry_price} (side={side})")

    while True:
        try:
            current_price = _get_current_price(symbol, broker_name)
            if not current_price:
                time.sleep(15)
                continue

            # Buy-side logic
            if side == "buy":
                best_price = max(best_price, current_price)
                trigger_price = best_price * (1 - threshold)
                if current_price <= trigger_price:
                    broker.cancel_order(order_id)
                    result = broker.place_order(symbol, qty, "sell")
                    _log_prediction_result(order_id, "SUCCESS")
                    _send_tp_alert(symbol, current_price, side, broker_name)
                    return result

            # Sell-side logic
            else:
                best_price = min(best_price, current_price)
                trigger_price = best_price * (1 + threshold)
                if current_price >= trigger_price:
                    broker.cancel_order(order_id)
                    result = broker.place_order(symbol, qty, "buy")
                    _log_prediction_result(order_id, "SUCCESS")
                    _send_tp_alert(symbol, current_price, side, broker_name)
                    return result

            time.sleep(15)

        except Exception as e:
            logging.error(f"[{symbol}] Trailing TP task failed: {e}")
            raise self.retry(exc=e, countdown=30)


def schedule_trailing_take_profit(symbol, qty, broker_name, side, order_id, trigger_pct):
    trailing_take_profit_task.delay(symbol, qty, broker_name, side, order_id, trigger_pct)


def _get_current_price(symbol, broker_name):
    try:
        pos = BROKER_MAP[broker_name].get_position(symbol)
        return float(pos["avg_price"]) if pos else None
    except Exception as e:
        logging.error(f"[{symbol}] Price fetch error: {e}")
        return None


def _log_prediction_result(order_id: str, result: str):
    try:
        db = SessionLocal()
        pred = db.query(Prediction).filter(Prediction.id == order_id).first()
        if pred:
            pred.feedback = PredictionFeedback[result.upper()]
            
            # Calculate profit % if position exists
            pos = pred.input_data or {}
            entry_price = pos.get("entry_price")
            exit_price = _get_current_price(pred.ticker, pred.model_name.lower())
            if entry_price and exit_price:
                try:
                    profit_pct = ((exit_price - entry_price) / entry_price) * 100 if pred.prediction == 1 else ((entry_price - exit_price) / entry_price) * 100
                    pred.rationale = f"{pred.rationale or ''} | Profit: {profit_pct:.2f}%"
                except Exception as e:
                    logging.warning(f"Profit calc error: {e}")

            db.commit()
            logging.info(f"[{pred.ticker}] Prediction result logged as {result.upper()}")
        db.close()
    except Exception as e:
        logging.error(f"[DB] Failed to log prediction result: {e}")


def _send_tp_alert(symbol, price, side, broker_name):
    msg = f"💰 [{symbol}] Trailing TP hit at {price:.4f} — {side.upper()} closed via {broker_name.upper()}"
    logging.info(msg)
    send_alert(msg)
