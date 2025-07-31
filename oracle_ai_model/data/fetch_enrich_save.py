# oracle_ai_model/data/fetch_enrich_save.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from oracle_ai_model.data.market_data import enrich_market_data

# DB imports
from backend_api.app.db.connection import SessionLocal
from backend_api.app.db.models import MarketSnapshotLog


def fetch_enrich_and_save(symbol: str, interval: str = "1d", period: str = "6mo") -> pd.DataFrame:
    db = SessionLocal()
    try:
        df = yf.download(symbol, period=period, interval=interval)
        if df.empty:
            raise ValueError(f"No data retrieved for symbol: {symbol}")
        
        enriched_df = enrich_market_data(df, symbol)

        # Log to DB
        log = MarketSnapshotLog(
            symbol=symbol,
            status="success",
            message="Data fetched and enriched",
            row_count=len(enriched_df)
        )
        db.add(log)
        db.commit()

        return enriched_df

    except Exception as e:
        # Log failure
        db.add(MarketSnapshotLog(
            symbol=symbol,
            status="error",
            message=str(e),
            row_count=0
        ))
        db.commit()
        raise e
    finally:
        db.close()
