# 📂 File: broker_execution/services/risk_management.py

import logging
from typing import Literal, Optional
import pandas as pd
from datetime import datetime
from utils.indicators import compute_atr
from db.models import RiskLevels
from db.connection import SessionLocal
from broker_execution.broker_metadata import BROKER_METADATA

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
        broker: str = "alpaca",
        debug: bool = False
    ):
        self.symbol = symbol.upper()
        self.entry_price = entry_price
        self.price_df = price_df
        self.strategy_id = strategy_id
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.trailing_pct = trailing_pct
        self.use_volatility = use_volatility
        self.position_type = position_type.lower()
        self.atr_sl_mult = atr_sl_mult
        self.atr_tp_mult = atr_tp_mult
        self.debug = debug
        self.high_price = entry_price
        self.low_price = entry_price
        self.broker = broker

        # Load broker-specific rules from metadata
        self.broker_rules = BROKER_METADATA.get(broker, {})
        self.leverage = self.broker_rules.get("max_leverage", 1.0)
        self.margin = self.broker_rules.get("margin_required", 1.0)
        self.fee_pct = self.broker_rules.get("commission", 0.0)

        # Compute SL/TP levels based on ATR or fixed % thresholds
        self.atr = float(compute_atr(self.price_df, period=14)[-1] or 0.0)
        self.stop_loss, self.take_profit = self._calculate_levels()
        self._adjust_for_broker()

        if self.debug:
            logging.info(f"[{self.symbol}] ATR={self.atr}, SL={self.stop_loss}, TP={self.take_profit}")

    def _adjust_for_broker(self):
        """Adjust SL/TP relative to leverage."""
        if self.leverage > 1:
            self.stop_loss = round(self.stop_loss * (1 / self.leverage), 4)
            self.take_profit = round(self.take_profit * (1 / self.leverage), 4)

    def _calculate_levels(self):
        """Calculate SL/TP using ATR or trailing %."""
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

    def estimate_net_profit(self, quantity: float, exit_price: float) -> float:
        """Estimate net profit after broker fee."""
        gross = (exit_price - self.entry_price) * quantity
        gross = gross if self.position_type == "long" else -gross
        fee = self.entry_price * quantity * self.fee_pct
        return round(gross - fee, 4)

    def audit_trade(self, quantity: float, exit_price: float):
        """Return a trade summary with broker costs applied."""
        net_profit = self.estimate_net_profit(quantity, exit_price)
        audit = {
            "symbol": self.symbol,
            "entry_price": self.entry_price,
            "exit_price": exit_price,
            "quantity": quantity,
            "profit": net_profit,
            "broker": self.broker,
            "leverage": self.leverage,
            "fee_pct": self.fee_pct,
            "timestamp": datetime.utcnow()
        }
        logging.info(f"📊 Trade audit: {audit}")
        return audit

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
