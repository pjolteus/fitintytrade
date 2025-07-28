import pandas as pd
import pandas_ta as ta
import yfinance as yf
import logging
from typing import List

from db.connection import SessionLocal
from models.feature_snapshot import FeatureSnapshot

DEFAULT_FEATURES = ["rsi", "macd", "ema", "bbands", "adx", "stochrsi"]

def get_features_for_ticker(
    ticker: str,
    interval: str,
    window_size: int,
    selected_features: List[str] = None,
    user_id: str = None  # Optional: for DB saving
) -> List[float]:
    """
    Extracts technical indicator features for a given ticker and interval.
    Optionally saves them to the database if user_id is provided.
    """
    try:
        selected_features = selected_features or DEFAULT_FEATURES
        interval_map = {
            "1m": "1m", "5m": "5m", "15m": "15m",
            "1h": "60m", "1d": "1d"
        }

        yf_interval = interval_map.get(interval, "1h")
        df = yf.download(ticker, period="7d", interval=yf_interval)

        if df.empty or len(df) < window_size + 30:
            raise ValueError(f"Not enough data for {ticker} ({len(df)} rows)")

        df_ind = pd.DataFrame(index=df.index)

        # -------------------- Core Indicators --------------------
        if "rsi" in selected_features:
            df_ind["rsi"] = ta.rsi(df["Close"], length=14)

        if "macd" in selected_features:
            macd = ta.macd(df["Close"], fast=12, slow=26, signal=9)
            df_ind["macd"] = macd["MACD"]

        if "ema" in selected_features:
            df_ind["ema"] = ta.ema(df["Close"], length=10)

        if "sma" in selected_features:
            df_ind["sma"] = ta.sma(df["Close"], length=10)

        if "volume" in selected_features:
            df_ind["volume"] = df["Volume"]

        # -------------------- Advanced Indicators --------------------
        if "bbands" in selected_features:
            bb = ta.bbands(df["Close"], length=20, std=2)
            df_ind["bb_upper"] = bb["BBU_20_2.0"]
            df_ind["bb_middle"] = bb["BBM_20_2.0"]
            df_ind["bb_lower"] = bb["BBL_20_2.0"]

        if "adx" in selected_features:
            df_ind["adx"] = ta.adx(df["High"], df["Low"], df["Close"], length=14)["ADX_14"]

        if "stochrsi" in selected_features:
            stochrsi = ta.stochrsi(df["Close"], length=14)
            df_ind["stochrsi_k"] = stochrsi["STOCHRSIk_14_14_3_3"]
            df_ind["stochrsi_d"] = stochrsi["STOCHRSId_14_14_3_3"]

        df_ind.dropna(inplace=True)
        recent = df_ind.tail(window_size)

        if len(recent) < window_size:
            raise ValueError("Not enough clean rows for indicator window")

        feature_values = recent.values.flatten().tolist()
        normalized = _normalize_sequence(feature_values)

        # Save to DB if user_id provided
        if user_id:
            save_feature_snapshot(user_id, ticker, interval, normalized)

        return normalized

    except Exception as e:
        logging.warning(f"Feature extraction failed for {ticker}: {e}")
        return [0.0] * window_size


def _normalize_sequence(seq: List[float]) -> List[float]:
    series = pd.Series(seq)
    return ((series - series.mean()) / (series.std() + 1e-6)).tolist()


def save_feature_snapshot(user_id: str, ticker: str, interval: str, features: List[float]):
    db = SessionLocal()
    try:
        snapshot = FeatureSnapshot(
            user_id=user_id,
            ticker=ticker,
            interval=interval,
            values=features
        )
        db.add(snapshot)
        db.commit()
        logging.info(f"Saved feature snapshot for {user_id} / {ticker}")
    except Exception as e:
        logging.error(f"Failed to save feature snapshot: {e}")
    finally:
        db.close()

