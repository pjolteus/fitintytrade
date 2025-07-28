from fastapi import APIRouter, Depends
from pydantic import BaseModel
import torch
import numpy as np
from sqlalchemy.orm import Session

from oracle_ai_model.utils.helpers import add_technical_indicators, normalize
from oracle_ai_model.data.loader import download_stock_data
from oracle_ai_model.models.model import LSTMModel
from oracle_ai_model.models.gru_model import GRUTimeSeriesModel
from oracle_ai_model.models.tcn_model import TCN
from oracle_ai_model.models.transformer_model import TransformerTimeSeriesModel

from db.engine import SessionLocal
from db.models import Prediction  # ✅ import your SQLAlchemy model

router = APIRouter()

# ✅ Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PredictionRequest(BaseModel):
    symbol: str
    model_type: str = "lstm"  # Options: lstm, gru, transformer, tcn

@router.post("/predict")
def predict_endpoint(request: PredictionRequest, db: Session = Depends(get_db)):
    symbol = request.symbol.upper()
    model_type = request.model_type.lower()
    try:
        df = download_stock_data(symbol, period="1mo")
        df = add_technical_indicators(df)
        df = normalize(df, ["Close", "rsi", "macd", "ema", "volatility"])

        seq_length = 24
        data = df[["Close", "rsi", "macd", "ema", "volatility"]].values
        X_input = np.expand_dims(data[-seq_length:], axis=0)
        X_tensor = torch.tensor(X_input).float()

        input_size = X_tensor.shape[2]
        model_path = f"{model_type}_model.pth"

        if model_type == "lstm":
            model = LSTMModel(input_size)
        elif model_type == "gru":
            model = GRUTimeSeriesModel(input_size)
        elif model_type == "tcn":
            model = TCN(input_size=input_size, num_channels=[32, 64])
        elif model_type == "transformer":
            model = TransformerTimeSeriesModel(input_size)
        else:
            return {"status": "error", "message": "Unsupported model type."}

        model.load_state_dict(torch.load(model_path))
        model.eval()

        with torch.no_grad():
            output = model(X_tensor)
            probability = torch.sigmoid(output).item()
            prediction = int(probability > 0.5)

        # ✅ Save prediction to the database
        pred_record = Prediction(
            symbol=symbol,
            model_type=model_type,
            prediction=prediction,
            probability=probability
        )
        db.add(pred_record)
        db.commit()
        db.refresh(pred_record)

        return {
            "status": "success",
            "symbol": symbol,
            "model_type": model_type,
            "prediction": prediction,
            "probability": probability,
            "id": pred_record.id  # ✅ return the DB ID
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
