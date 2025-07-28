from sqlalchemy import Column, String, Integer, DateTime, JSON
from datetime import datetime
from db.connection import Base

class FeatureSnapshot(Base):
    __tablename__ = "feature_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    ticker = Column(String)
    interval = Column(String)
    values = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
