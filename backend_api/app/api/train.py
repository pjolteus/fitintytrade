
from fastapi import APIRouter, Query
from oracle_ai_model.train.train_model import train
import os

router = APIRouter()

@router.post("/train")
def train_model_endpoint(model_type: str = Query("lstm", enum=["lstm", "gru", "transformer", "tcn"])):
    os.environ["MODEL_TYPE"] = model_type
    try:
        train()
        return {"status": "success", "message": f"{model_type.upper()} model trained successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
