from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from db.models.alert_log import AlertLog
from db.models.prediction import Prediction
from dependencies.auth import get_current_user
from schemas.auth import User

router = APIRouter()

@router.get("/admin/alerts", tags=["Admin"])
async def get_alerts(limit: int = 100, user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    db: Session = SessionLocal()
    alerts = db.query(AlertLog).order_by(AlertLog.timestamp.desc()).limit(limit).all()
    db.close()
    return alerts

@router.get("/admin/predictions", tags=["Admin"])
async def get_predictions(limit: int = 100, user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    db: Session = SessionLocal()
    preds = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(limit).all()
    db.close()
    return preds
