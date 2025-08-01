from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
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
from db.models import Prediction

from broker_execution.strategies.trade_selector import select_top_trades_with_allocation
from services.train_service import enqueue_training

from app.schemas.prediction import PredictionOutput

router = APIRouter()

# ✅ Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Request schema
class PredictionRequest(BaseModel):
    symbol: str
    model_type: str = "lstm"  # lstm, gru, transformer, tcn
    asset_type: str = "stock"  # stock, currency, crypto

@router.post("/predict", response_model=List[PredictionOutput])
def predict_endpoint(
    requests: List[PredictionRequest],
    db: Session = Depends(get_db),
    filter_top: bool = Query(False, description="Return only top filtered predictions")
):
    predictions = []

    for req in requests:
        symbol = req.symbol.upper()
        model_type = req.model_type.lower()
        asset_type = req.asset_type

        try:
            # Step 1: Load + prepare data
            df = download_stock_data(symbol, period="1mo")
            df = add_technical_indicators(df)
            df = normalize(df, ["Close", "rsi", "macd", "ema", "volatility"])
            data = df[["Close", "rsi", "macd", "ema", "volatility"]].values
            X_input = np.expand_dims(data[-24:], axis=0)
            X_tensor = torch.tensor(X_input).float()

            # Step 2: Select model
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
                continue  # Skip unsupported

            model.load_state_dict(torch.load(model_path))
            model.eval()

            # Step 3: Predict
            with torch.no_grad():
                output = model(X_tensor)
                prob = torch.sigmoid(output).item()
                pred_class = int(prob > 0.5)

            # Step 4: Save prediction
            pred_record = Prediction(
                symbol=symbol,
                model_type=model_type,
                prediction=pred_class,
                probability=prob
            )
            db.add(pred_record)
            db.commit()
            db.refresh(pred_record)

            # Step 5: Format output
            predictions.append({
                "ticker": symbol,
                "asset_type": asset_type,
                "prediction": pred_class,
                "confidence": prob,
                "entry_point": None,
                "exit_point": None,
                "model_type": model_type,
                "generated_at": pred_record.created_at or datetime.utcnow(),
            })

            # ✅ Step 6: Trigger auto-retrain
            enqueue_training([symbol], model_type=model_type)

        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            continue

    # Step 7: Apply filtering logic if requested
    if filter_top:
        predictions = select_top_trades_with_allocation(
            predictions=predictions,
            total_capital=10000,
            top_n=6,
            min_confidence=0.6,
            exclude_bankrupt=True,
            diversify_by="asset_type",
            allocation_method="score_weighted"
        )

    return predictions
