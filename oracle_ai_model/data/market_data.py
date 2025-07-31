# oracle_ai_model/data/market_data.py

import os
import pandas as pd
from .cleaner import clean_data
from .snapshot import save_snapshot
from oracle_ai_model.utils.indicators import compute_atr


def enrich_market_data(df: pd.DataFrame, symbol: str, save: bool = True, folder: str = "oracle_ai_model/data/snapshots") -> pd.DataFrame:
    """
    Clean, enrich with ATR, and optionally save the snapshot.

    Args:
        df (pd.DataFrame): Raw market data (must contain High, Low, Close).
        symbol (str): Ticker symbol for saving snapshot.
        save (bool): Whether to save the enriched snapshot.
        folder (str): Directory to save the file.

    Returns:
        pd.DataFrame: Cleaned and enriched market data.
    """
    if df.empty or not all(col in df.columns for col in ["High", "Low", "Close"]):
        raise ValueError("DataFrame must contain 'High', 'Low', and 'Close' columns.")

    df = clean_data(df)
    df = compute_atr(df, period=14)  # Adds 'atr' column

    if save:
        save_snapshot(df, name=symbol, folder=folder)

    return df
