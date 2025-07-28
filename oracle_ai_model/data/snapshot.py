# data/cleaner.py
import pandas as pd

def clean_data(df):
    df = df.dropna()
    df = df[df.select_dtypes(include=['number']).apply(lambda x: ~x.isin([float('inf'), float('-inf')])).all(axis=1)]
    df = df.sort_values(by=df.columns[0])  # Sort by time/index
    df = df.reset_index(drop=True)
    return df


# data/snapshot.py
import os

def save_snapshot(df, name, folder="data/snapshots"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.csv")
    df.to_csv(path, index=False)
    print(f"Snapshot saved: {path}")


# data/sources.py
# Future extension to OANDA, Alpha Vantage, or Alpaca

def fetch_from_oanda(symbol, interval):
    # TODO: Use OANDA API
    raise NotImplementedError("OANDA integration not implemented yet")

def fetch_from_alpaca(symbol, interval):
    # TODO: Use Alpaca API for live stock
    raise NotImplementedError("Alpaca integration not implemented yet")
