from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional, List

from app.schemas.prediction import PredictionInput, PredictionOutput
from app.schemas.train import TrainRequest, TrainResponse
from app.schemas.status import StatusResponse, ModelInfoResponse
from app.schemas.auth import User

from app.dependencies.auth import get_current_user
from services.predict_service import run_prediction, get_feature_importance
from services.train_service import enqueue_training
from services.history_service import fetch_prediction_history

from app.api.execute import router as execute_router  # Broker execution subrouter
from app.api.predict import predict_endpoint  # Use batch-aware endpoint

router = APIRouter()

# ----------------------------
# POST /predict (Batch + Filter Top Trades)
# ----------------------------
@router.post("/predict", response_model=List[PredictionOutput], tags=["Prediction"])
async def predict(
    data: List[PredictionInput],
    filter_top: bool = Query(False, description="Filter and return only top trades"),
    user: User = Depends(get_current_user)
):
    try:
        # Pass user context and filtering option to backend logic
        result = await predict_endpoint(requests=data, db=None, filter_top=filter_top)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# ----------------------------
# POST /train
# ----------------------------
@router.post("/train", response_model=TrainResponse, tags=["Training"])
async def train_model(request: TrainRequest, user: User = Depends(get_current_user)):
    try:
        task_id = enqueue_training(request.model_type)
        return {"message": "Training started", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


# ----------------------------
# GET /status
# ----------------------------
@router.get("/status", response_model=StatusResponse, tags=["System"])
async def get_status():
    return {
        "status": "online",
        "model": "Transformer-v2",
        "last_trained": "2025-07-19T14:30:00Z",
        "uptime": "13h 44m"
    }


# ----------------------------
# GET /model-info
# ----------------------------
@router.get("/model-info", response_model=ModelInfoResponse, tags=["System"])
async def get_model_info():
    return {
        "model_name": "Transformer-v2",
        "model_type": "Transformer",
        "trained_on": "2025-07-19T14:30:00Z",
        "accuracy": 0.872,
        "f1_score": 0.859
    }


# ----------------------------
# GET /predictions
# ----------------------------
@router.get("/predictions", tags=["History"])
async def get_predictions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort_by: Optional[str] = Query("timestamp", pattern="^(timestamp|confidence)$"),
    order: Optional[str] = Query("desc", pattern="^(asc|desc)$"),
    user: User = Depends(get_current_user)
):
    try:
        items, total = fetch_prediction_history(
            user_id=user.id,
            page=page,
            limit=limit,
            sort_by=sort_by,
            order=order
        )
        return {"items": items, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching prediction history")


# ----------------------------
# GET /predict/explain
# ----------------------------
@router.get("/predict/explain", tags=["Prediction"])
async def explain_prediction(user: User = Depends(get_current_user)):
    try:
        explanation = get_feature_importance()
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail="Explainability not available yet")


# ----------------------------
# Mount broker execution endpoints
# ----------------------------
router.include_router(execute_router)
