from pydantic import BaseModel, Field
from typing import Optional, Dict, Literal
from datetime import datetime

class PredictionOutput(BaseModel):
    ticker: str = Field(..., example="AAPL")
    prediction: Literal[0, 1] = Field(..., description="0 = Bearish/Put, 1 = Bullish/Call", example=1)
    confidence: float = Field(..., ge=0, le=1, example=0.87)
    confidence_band: Optional[Dict[str, float]] = Field(
        None,
        example={"lower": 0.74, "upper": 0.95},
        description="Optional confidence interval"
    )
    rationale: Optional[str] = Field(
        None,
        example="Strong momentum and bullish crossover detected",
        description="Explanation from model or rules"
    )
    timestamp: datetime = Field(..., example="2025-07-20T15:32:00Z")
    model_name: str = Field(..., example="Transformer-v2")
    model_version: Optional[str] = Field("v2.1.0", example="v2.1.0")
    prediction_type: Optional[Literal["Buy/Sell", "Up/Down", "Score"]] = Field("Buy/Sell")
    features_used: Optional[Dict[str, float]] = Field(
        None,
        example={"rsi": 0.2, "macd": 0.3, "volume": 0.1},
        description="Feature importance scores (if available)"
    )
    source_model_version: Optional[str] = Field(
        None,
        example="transformer_v2_checkpoint_20250719.pt",
        description="Model file or checkpoint name"
    )

    class Config:
        schema_extra = {
            "example": {
                "ticker": "AAPL",
                "prediction": 1,
                "confidence": 0.87,
                "confidence_band": {"lower": 0.74, "upper": 0.95},
                "rationale": "Strong momentum and bullish crossover detected",
                "timestamp": "2025-07-20T15:32:00Z",
                "model_name": "Transformer-v2",
                "model_version": "v2.1.0",
                "prediction_type": "Buy/Sell",
                "features_used": {"rsi": 0.2, "macd": 0.3, "volume": 0.1},
                "source_model_version": "transformer_v2_checkpoint_20250719.pt"
            }
        }

