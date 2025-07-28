from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    JSON,
    Enum as SQLEnum,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from db.connection import Base


class PredictionFeedback(Enum):
    UNKNOWN = "unknown"
    SUCCESS = "success"
    FAILURE = "failure"


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    ticker = Column(String, nullable=False)
    interval = Column(String, nullable=False)
    prediction = Column(Integer, nullable=False)  # 0 or 1
    confidence = Column(Float, nullable=False)
    confidence_band = Column(JSON, nullable=True)
    rationale = Column(String, nullable=True)

    input_data = Column(JSON, nullable=True)  # Raw features used
    model_name = Column(String, default="LSTM-v1")
    model_version = Column(String, default="1.0.0")

    feedback = Column(SQLEnum(PredictionFeedback), default=PredictionFeedback.UNKNOWN)
    active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship (if you have a User model)
    user = relationship("User", back_populates="predictions")

    def __repr__(self):
        return f"<Prediction {self.id} | {self.ticker} | {self.prediction} ({self.confidence:.2f})>"

