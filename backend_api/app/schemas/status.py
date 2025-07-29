from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StatusResponse(BaseModel):
    status: str = Field(..., description="Overall system health status")
    uptime: Optional[str] = Field(None, description="System uptime in human-readable format")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Current server timestamp")
    active_workers: Optional[int] = Field(None, description="Number of active Celery workers or jobs")
    db_status: Optional[str] = Field(None, description="Database connection status")
    redis_status: Optional[str] = Field(None, description="Redis broker status")


class ModelInfoResponse(BaseModel):
    model_type: str = Field(..., description="Model type (e.g., LSTM, Transformer, GRU)")
    version: Optional[str] = Field(None, description="Model version or hash")
    last_trained: Optional[datetime] = Field(None, description="When the model was last trained")
    accuracy: Optional[float] = Field(None, description="Validation accuracy of the current model")
    f1_score: Optional[float] = Field(None, description="F1 score of the model if applicable")
    is_live: bool = Field(..., description="Whether this model is currently in production")




