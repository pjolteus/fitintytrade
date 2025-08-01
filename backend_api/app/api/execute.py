from fastapi import APIRouter, HTTPException, Depends
from app.schemas.execution import TradeRequest, TradeResponse
from app.dependencies.auth import get_current_user
from app.services.strategy_executor import schedule_trailing_take_profit
from connectors import alpaca, oanda, ibr, fxcm, binance, bybit, coinbase

router = APIRouter()

# Map broker names to connector modules
BROKER_MAP = {
    "alpaca": alpaca,
    "oanda": oanda,
    "ibr": ibr,
    "fxcm": fxcm,
    "binance": binance,
    "bybit": bybit,
    "coinbase": coinbase
}

@router.post("/execute-trade", response_model=TradeResponse, tags=["Execution"])
async def execute_trade(request: TradeRequest, user=Depends(get_current_user)):
    broker_name = request.broker.lower()
    if broker_name not in BROKER_MAP:
        raise HTTPException(status_code=400, detail="❌ Unsupported broker")

    broker = BROKER_MAP[broker_name]

    try:
        # Place the trade with optional parameters
        result = broker.place_order(
            symbol=request.symbol,
            qty=request.qty,
            side=request.side,
            stop_loss=request.stop_loss,
            take_profit=request.take_profit,
            trailing_stop=request.trailing_stop,
            trailing_take_profit=request.trailing_take_profit,
            leverage=request.leverage,
            margin_mode=request.margin_mode  # "isolated" or "cross"
        )

        # Optional: Schedule trailing TP monitor
        if request.trailing_take_profit:
            schedule_trailing_take_profit(
                symbol=request.symbol,
                qty=request.qty,
                broker_name=broker_name,
                side=request.side,
                order_id=result.get("orderId"),
                trigger_pct=request.trailing_take_profit
            )

        return {
            "broker": broker_name,
            "orderId": result.get("orderId"),
            "status": result.get("status")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"🚨 Trade execution failed: {str(e)}")


# Optional utility endpoints:

@router.get("/order-status", tags=["Execution"])
async def order_status(broker: str, order_id: str):
    broker = broker.lower()
    if broker not in BROKER_MAP:
        raise HTTPException(status_code=400, detail="❌ Unsupported broker")
    try:
        return BROKER_MAP[broker].get_order_status(order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch order status: {str(e)}")


@router.post("/cancel-order", tags=["Execution"])
async def cancel_order(broker: str, order_id: str):
    broker = broker.lower()
    if broker not in BROKER_MAP:
        raise HTTPException(status_code=400, detail="❌ Unsupported broker")
    try:
        return BROKER_MAP[broker].cancel_order(order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel order: {str(e)}")
