# data/loader.py

import yfinance as yf
import pandas as pd
import os
from datetime import datetime
from .cleaner import clean_data
from .snapshot import save_snapshot

# Placeholder for live forex or broker APIs (to be implemented)
def get_live_forex_data(symbol, interval="1d", outputsize="compact"):
    # TODO: Connect to OANDA or Alpha Vantage
    raise NotImplementedError("Live Forex data fetch not yet implemented")

def get_live_stock_data(symbol, interval="1d"):
    # Placeholder for broker-based real-time stock data
    raise NotImplementedError("Live Stock data fetch not yet implemented")

def download_stock_data(symbol, period="1mo", interval="1d"):
    print(f"Downloading stock data for {symbol}...")
    df = yf.download(symbol, period=period, interval=interval)
    df = df.reset_index()
    df["symbol"] = symbol
    return df

def load_forex_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Forex data file not found: {path}")
    df = pd.read_csv(path, parse_dates=["Date"])
    return df

def load_data(symbol, market="stock", interval="1d", live=False, snapshot=False):
    if market == "stock":
        df = get_live_stock_data(symbol, interval) if live else download_stock_data(symbol, period="1mo", interval=interval)
    elif market == "forex":
        df = get_live_forex_data(symbol, interval) if live else load_forex_csv(f"data/forex/{symbol}.csv")
    else:
        raise ValueError("Market must be either 'stock' or 'forex'")

    df = clean_data(df)

    if snapshot:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        save_snapshot(df, f"{symbol}_{timestamp}")

    return df
