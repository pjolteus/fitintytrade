from pydantic import BaseModel, Field
from typing import Optional, Literal, List

class PredictionInput(BaseModel):
    ticker: str = Field(..., example="EURUSD")
    interval: Literal["1m", "5m", "15m", "1h", "1d"] = Field(..., example="1h")
    window_size: Optional[int] = Field(60, description="Number of time steps to consider", example=60)
    features: Optional[List[str]] = Field(
        None,
        description="Optional list of features to use",
        example=["rsi", "macd", "volume"]
    )

    class Config:
        schema_extra = {
            "example": {
                "ticker": "AAPL",
                "interval": "15m",
                "window_size": 90,
                "features": ["rsi", "ema", "macd"]
            }
        }

