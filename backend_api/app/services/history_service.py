from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from db.connection import SessionLocal
from db.models.prediction import Prediction
from typing import List, Tuple, Dict


def serialize_prediction(pred: Prediction) -> Dict:
    return {
        "ticker": pred.ticker,
        "prediction": pred.prediction,
        "confidence": pred.confidence,
        "confidence_band": pred.confidence_band,
        "rationale": pred.rationale,
        "timestamp": pred.created_at.isoformat(),
        "model_name": pred.model_name,
        "model_version": pred.model_version,
        "prediction_type": pred.prediction_type,
        "features_used": pred.features_used,
        "source_model_version": pred.source_model_version,
    }


def fetch_prediction_history(
    user_id: str,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "timestamp",
    order: str = "desc"
) -> Tuple[List[Dict], int]:
    db: Session = SessionLocal()

    # Choose sort column
    sort_column = {
        "timestamp": Prediction.created_at,
        "confidence": Prediction.confidence
    }.get(sort_by, Prediction.created_at)

    order_by = desc(sort_column) if order == "desc" else asc(sort_column)

    try:
        # Count total records for pagination
        total = db.query(Prediction).filter(Prediction.user_id == user_id).count()

        # Fetch paginated + sorted records
        predictions = (
            db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .order_by(order_by)
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        # Convert to serializable format
        return [serialize_prediction(p) for p in predictions], total

    finally:
        db.close()
