
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
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
