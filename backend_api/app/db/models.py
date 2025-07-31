# backend_api/app/db/models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    model_type = Column(String)
    prediction = Column(Integer)
    probability = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class MarketSnapshotLog(Base):
    __tablename__ = "market_snapshot_logs"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    status = Column(String)  # 'success' or 'error'
    message = Column(Text, nullable=True)
    row_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

