from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime

class PredictionInput(BaseModel):
    ticker: str = Field(..., description="Asset symbol (e.g., AAPL, EUR/USD, BTC-USD)")
    model_type: Literal["LSTM", "Transformer", "GRU", "TCN"] = Field(..., description="AI model to use for prediction")
    asset_type: Literal["stock", "currency", "crypto"] = Field(..., description="Type of asset to analyze")
    timestamp: Optional[datetime] = Field(None, description="Optional prediction timestamp override")

    @validator("ticker")
    def ticker_format(cls, v):
        if not v or len(v) < 2:
            raise ValueError("Ticker symbol is too short or missing.")
        return v.upper()


class PredictionOutput(BaseModel):
    ticker: str = Field(..., description="Asset symbol")
    asset_type: str = Field(..., description="Asset class: stock, currency, or crypto")
    prediction: Literal[0, 1] = Field(..., description="Prediction class: 1 = Call/Buy, 0 = Put/Sell")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the prediction")
    entry_point: Optional[float] = Field(None, description="Suggested entry price")
    exit_point: Optional[float] = Field(None, description="Suggested exit price")
    model_type: str = Field(..., description="Model used to generate prediction")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of prediction generation")



