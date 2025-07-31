import logging
from typing import Literal, Optional
import pandas as pd
from datetime import datetime
from utils.indicators import compute_atr  # Assumes ATR is defined
from db.models import RiskLevels  # SQLAlchemy ORM
from db.connection import SessionLocal

class TradeRiskManager:
    def __init__(
        self,
        symbol: str,
        entry_price: float,
        price_df: pd.DataFrame,
        strategy_id: Optional[str] = None,
        stop_loss_pct: float = 0.02,
        take_profit_pct: float = 0.05,
        trailing_pct: float = 0.015,
        use_volatility: bool = True,
        position_type: Literal["long", "short"] = "long",
        atr_sl_mult: float = 1.0,
        atr_tp_mult: float = 2.0,
        debug: bool = False
    ):
        self.symbol = symbol.upper()
        self.entry_price = entry_price
        self.strategy_id = strategy_id
        self.trailing_pct = trailing_pct
        self.use_volatility = use_volatility
        self.position_type = position_type.lower()
        self.price_df = price_df
        self.high_price = entry_price
        self.low_price = entry_price
        self.atr_sl_mult = atr_sl_mult
        self.atr_tp_mult = atr_tp_mult
        self.debug = debug

        self.atr = float(compute_atr(self.price_df, period=14)[-1] or 0.0)
        self.stop_loss, self.take_profit = self._calculate_levels()

        if self.debug:
            logging.info(f"[{self.symbol}] ATR={self.atr}, SL={self.stop_loss}, TP={self.take_profit}")

    def _calculate_levels(self):
        if self.use_volatility and self.atr > 0:
            if self.position_type == "long":
                sl = self.entry_price - (self.atr * self.atr_sl_mult)
                tp = self.entry_price + (self.atr * self.atr_tp_mult)
            else:
                sl = self.entry_price + (self.atr * self.atr_sl_mult)
                tp = self.entry_price - (self.atr * self.atr_tp_mult)
        else:
            if self.position_type == "long":
                sl = self.entry_price * (1 - self.trailing_pct)
                tp = self.entry_price * (1 + self.trailing_pct * 2)
            else:
                sl = self.entry_price * (1 + self.trailing_pct)
                tp = self.entry_price * (1 - self.trailing_pct * 2)

        return round(sl, 4), round(tp, 4)

    def update_trailing_stop(self, current_price: float) -> float:
        if self.position_type == "long":
            self.high_price = max(self.high_price, current_price)
            trailing_sl = self.high_price * (1 - self.trailing_pct)
        else:
            self.low_price = min(self.low_price, current_price)
            trailing_sl = self.low_price * (1 + self.trailing_pct)
        return round(trailing_sl, 4)

    def get_current_levels(self, current_price: float) -> dict:
        trailing_sl = self.update_trailing_stop(current_price)
        data = {
            "symbol": self.symbol,
            "entry_price": round(self.entry_price, 4),
            "static_sl": self.stop_loss,
            "static_tp": self.take_profit,
            "trailing_sl": trailing_sl,
            "timestamp": datetime.utcnow()
        }
        if self.debug:
            logging.info(f"[{self.symbol}] Risk snapshot: {data}")
        return data

    def save_to_db(self, levels: dict):
        try:
            with SessionLocal() as db:
                risk_record = RiskLevels(**levels, strategy_id=self.strategy_id)
                db.add(risk_record)
                db.commit()
                if self.debug:
                    logging.info(f"✅ Saved risk levels for {self.symbol} to DB")
        except Exception as e:
            logging.error(f"❌ DB save failed for {self.symbol}: {e}")
