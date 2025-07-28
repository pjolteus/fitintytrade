from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from db.connection import Base

class TrainingLog(Base):
    __tablename__ = "training_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_type = Column(String, nullable=False)
    model_version = Column(String, default="v1.0.0")
    accuracy = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    loss = Column(Float, nullable=True)
    duration = Column(Float, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
