# backend_api/app/schemas/train.py

from pydantic import BaseModel
from typing import List, Optional

class TrainRequest(BaseModel):
    tickers: List[str]
    model_type: str  # e.g., "LSTM", "GRU", "Transformer"
    epochs: Optional[int] = 10
    batch_size: Optional[int] = 32
    learning_rate: Optional[float] = 0.001
    use_augmentation: Optional[bool] = False

class TrainResponse(BaseModel):
    model_id: str
    status: str
    accuracy: Optional[float] = None
    f1_score: Optional[float] = None
    message: Optional[str] = None


