from pydantic import BaseModel, Field
from typing import Optional

class TradeRequest(BaseModel):
    broker: str = Field(..., example="binance")
    symbol: str = Field(..., example="BTCUSDT")
    qty: float = Field(..., example=0.01)
    side: str = Field(..., example="buy", description="buy or sell")
    
    # Risk management
    stop_loss: Optional[float] = Field(None, example=28000.0)
    take_profit: Optional[float] = Field(None, example=32000.0)
    trailing_stop: Optional[float] = Field(None, example=1.5, description="Trailing stop percent")
    trailing_take_profit: Optional[float] = Field(None, example=2.0, description="Trailing take-profit percent")

    # Margin & leverage
    leverage: Optional[int] = Field(None, example=5, description="Leverage (for margin trading)")
    margin_mode: Optional[str] = Field("isolated", example="cross", description="Margin mode: isolated or cross")


class TradeResponse(BaseModel):
    broker: str = Field(..., example="binance")
    orderId: str = Field(..., example="abc123xyz")
    status: str = Field(..., example="submitted")

