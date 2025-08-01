from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime
from broker_execution.strategies.trade_selector import select_top_trades_with_allocatio

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


top_trades = select_top_trades_with_allocation(
    predictions=model_outputs,  # ← list of prediction dicts from AI
    total_capital=10000,
    top_n=6,
    min_confidence=0.6,
    exclude_bankrupt=True,
    diversify_by="asset_type",  # can also use 'sector' or 'pair'
    allocation_method="score_weighted"
)
