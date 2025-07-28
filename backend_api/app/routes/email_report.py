# backend/routes/email_report.py
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.models import Prediction
from backend.utils.email_utils import send_prediction_report_email

router = APIRouter()

class EmailReportRequest(BaseModel):
    prediction_ids: List[int]
    recipient_email: str

@router.post("/email-report")
async def email_prediction_report(payload: EmailReportRequest, db: AsyncSession = Depends(get_db)):
    if not payload.prediction_ids:
        raise HTTPException(status_code=400, detail="No prediction IDs provided.")

    result = await db.execute(
        Prediction.__table__.select().where(Prediction.id.in_(payload.prediction_ids))
    )
    predictions = result.fetchall()

    if not predictions:
        raise HTTPException(status_code=404, detail="Predictions not found.")

    await send_prediction_report_email(predictions, payload.recipient_email)
    return {"status": "success", "message": f"Report sent to {payload.recipient_email}"}
