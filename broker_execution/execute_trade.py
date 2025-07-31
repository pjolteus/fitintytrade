
# 📂 File: backend_api/broker_execution/execute_trade.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from broker_execution.connectors import alpaca, oanda, ibr, fxcm, bybit, binance, coinbase
from services.risk_management import TradeRiskManager
from services.market_data import get_recent_price_df
from datetime import datetime
from typing import Literal, Optional

router = APIRouter()

# -------------------------------
# 📦 Input Schema for Execution
# -------------------------------
class TradeRequest(BaseModel):
    symbol: str
    side: Literal["buy", "sell"]
    quantity: float
    broker: Literal["alpaca", "oanda", "ibr", "fxcm", "bybit", "binance", "coinbase"]
    leverage: Optional[float] = 1.0
    trailing_sl: Optional[bool] = False
    isolated: Optional[bool] = True
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

# -------------------------------
# 🔌 Broker Selector
# -------------------------------
BROKER_MAP = {
    "alpaca": alpaca,
    "oanda": oanda,
    "ibr": ibr,
    "fxcm": fxcm,
    "bybit": bybit,
    "binance": binance,
    "coinbase": coinbase,
}

# -------------------------------
# 🚀 Execute Trade Endpoint
# -------------------------------
@router.post("/execute-trade")
async def execute_trade(request: TradeRequest):
    broker = BROKER_MAP.get(request.broker)
    if not broker:
        raise HTTPException(status_code=400, detail="Unsupported broker")

    try:
        # 🧠 Pull recent price data for volatility-based SL/TP
        price_df = get_recent_price_df(request.symbol)

        # 🛡️ Apply Trade Risk Management Strategy
        entry_price = price_df["Close"].iloc[-1]
        manager = TradeRiskManager(
            symbol=request.symbol,
            entry_price=entry_price,
            price_df=price_df,
            stop_loss_pct=0.02,
            take_profit_pct=0.05,
            trailing_pct=0.015,
            use_volatility=True,
            position_type="long" if request.side == "buy" else "short",
            strategy_id=f"api:{datetime.utcnow().isoformat()}"
        )
        levels = manager.get_current_levels(current_price=entry_price)
        manager.save_to_db(levels)

        # 🧾 Place trade with risk-managed SL/TP
        order_id = broker.place_order(
            symbol=request.symbol,
            side=request.side,
            quantity=request.quantity,
            leverage=request.leverage,
            trailing_sl=request.trailing_sl,
            isolated=request.isolated,
            stop_loss=request.stop_loss or levels["static_sl"],
            take_profit=request.take_profit or levels["static_tp"]
        )

        return {
            "status": "success",
            "order_id": order_id,
            "risk_levels": levels
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------
# ❌ Cancel Order
# -------------------------------
@router.post("/cancel-order")
async def cancel_order(broker: str, order_id: str):
    if broker not in BROKER_MAP:
        raise HTTPException(status_code=400, detail="Unsupported broker")
    try:
        result = BROKER_MAP[broker].cancel_order(order_id)
        return {"status": "cancelled", "order_id": order_id, "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------
# 📊 Order Status
# -------------------------------
@router.get("/order-status")
async def get_order_status(broker: str, order_id: str):
    if broker not in BROKER_MAP:
        raise HTTPException(status_code=400, detail="Unsupported broker")
    try:
        status = BROKER_MAP[broker].get_order_status(order_id)
        return {"order_id": order_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
