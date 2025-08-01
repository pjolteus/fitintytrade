from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    JSON,
    Enum as SQLEnum,
    Boolean,
    Text
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from enum import Enum

# Define Base here if not imported from elsewhere
Base = declarative_base()


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


class MarketSnapshotLog(Base):
    __tablename__ = "market_snapshot_logs"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    status = Column(String)  # 'success' or 'error'
    message = Column(Text, nullable=True)
    row_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=func.now())
