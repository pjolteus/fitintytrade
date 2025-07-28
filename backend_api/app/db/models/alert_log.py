from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from db.connection import Base

class AlertLog(Base):
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # e.g. "TP_HIT", "ERROR", "CLOSE_POSITION"
    symbol = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
