# backend_api/app/schemas/train.py

from pydantic import BaseModel, Field, conlist, conint, confloat
from typing import List, Optional
from enum import Enum


class ModelType(str, Enum):
    LSTM = "LSTM"
    GRU = "GRU"
    Transformer = "Transformer"
    TCN = "TCN"


class TrainRequest(BaseModel):
    tickers: conlist(str, min_items=1) = Field(..., description="List of ticker symbols to train on")
    model_type: ModelType = Field(..., description="Type of model to train (e.g., LSTM, GRU)")
    epochs: conint(gt=0) = Field(10, description="Number of training epochs")
    batch_size: conint(gt=0) = Field(32, description="Batch size for training")
    learning_rate: confloat(gt=0) = Field(0.001, description="Learning rate for optimizer")
    use_augmentation: Optional[bool] = Field(False, description="Whether to apply data augmentation")


class TrainResponse(BaseModel):
    model_id: str = Field(..., description="Unique identifier for the trained model")
    status: str = Field(..., description="Training status: success/failure")
    accuracy: Optional[float] = Field(None, description="Model accuracy on validation data")
    f1_score: Optional[float] = Field(None, description="F1 score on validation data")
    message: Optional[str] = Field(None, description="Additional info or error details")



