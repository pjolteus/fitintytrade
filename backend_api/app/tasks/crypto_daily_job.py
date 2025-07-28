# tasks/crypto_daily_job.py

from celery_app import celery_app
from services.feature_extraction import get_features_for_ticker
from oracle_ai_model.predict_from_model import run_lstm_prediction
from strategies.trade_selector import select_top_trades
from strategies.risk_management import apply_risk_management
from broker_execution.crypto_executor import execute_crypto_trade
from services.crypto_loader import get_top_crypto_symbols

@celery_app.task(name="tasks.crypto_daily_job.run_auto_crypto_trading")
def run_auto_crypto_trading():
    top_symbols = get_top_crypto_symbols(limit=30)
    predictions = []

    for symbol in top_symbols:
        try:
            features = get_features_for_ticker(symbol, interval="1h", market_type="crypto")
            result = run_lstm_prediction(ticker=symbol, features=features)
            result["market_type"] = "crypto"
            result["sentiment_score"] = 1.0  # placeholder
            predictions.append(result)
        except Exception as e:
            print(f"Error processing {symbol}: {e}")

    top_trades = select_top_trades(predictions, top_n=6)

    for trade in top_trades:
        sl_tp = apply_risk_management(entry_price=trade["entry_price"], ticker=trade["ticker"])
        trade.update(sl_tp)
        execute_crypto_trade(trade)
