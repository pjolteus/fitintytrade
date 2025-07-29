from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PredictionInput(BaseModel):
    ticker: str = Field(..., description="Ticker symbol for the asset (e.g., AAPL, EUR/USD)")
    model_type: str = Field(..., description="The AI model to use for prediction (e.g., 'LSTM', 'Transformer')")
    date: Optional[datetime] = Field(None, description="Optional date to perform prediction on (defaults to latest available)")

class PredictionOutput(BaseModel):
    ticker: str
    prediction: int = Field(..., description="Predicted class (1 for Call/Buy, 0 for Put/Sell)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level of the prediction")
    entry_point: Optional[float] = Field(None, description="Suggested entry price for trade")
    exit_point: Optional[float] = Field(None, description="Suggested exit price for trade")
    model_type: Optional[str] = Field(None, description="The model that produced the prediction")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time when prediction was generated")

