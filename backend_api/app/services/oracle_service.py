import torch
import time
import logging
from typing import List, Dict, Union
from tenacity import retry, stop_after_attempt, wait_fixed

from models.lstm_model import LSTMModel
from schemas.response import PredictionOutput
from datetime import datetime

# ----------------------
# Globals
# ----------------------
_model = None
_model_loaded = False
MODEL_PATH = "models/lstm_model.pth"

# ----------------------
# Retry Decorator
# ----------------------
@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def safe_model_predict(input_tensor: torch.Tensor) -> torch.Tensor:
    return _model(input_tensor)

# ----------------------
# Load the LSTM model once
# ----------------------
def load_model() -> None:
    global _model, _model_loaded
    if not _model_loaded:
        try:
            _model = LSTMModel()
            _model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
            _model.eval()
            _model_loaded = True
            logging.info(f"Model loaded successfully from {MODEL_PATH}")
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            _model_loaded = False

# ----------------------
# Normalize the input
# ----------------------
def normalize_input(data: List[float]) -> torch.Tensor:
    tensor = torch.tensor(data, dtype=torch.float32)
    return (tensor - tensor.mean()) / (tensor.std() + 1e-6)

# ----------------------
# Main Predict Function
# ----------------------
def run_lstm_prediction(ticker: str, features: List[float]) -> Union[PredictionOutput, Dict]:
    load_model()

    if not _model_loaded:
        return _fallback_response(ticker, "model_load_failed")

    try:
        input_tensor = normalize_input(features).unsqueeze(0).unsqueeze(-1)  # (batch, seq_len, 1)
        start = time.time()
        with torch.no_grad():
            output = safe_model_predict(input_tensor)
        elapsed = time.time() - start

        prob = torch.sigmoid(output).item()
        prediction = 1 if prob > 0.5 else 0
        confidence_band = {"lower": max(0, prob - 0.1), "upper": min(1, prob + 0.1)}

        return PredictionOutput(
            ticker=ticker,
            prediction=prediction,
            confidence=prob,
            confidence_band=confidence_band,
            rationale="LSTM pattern detection",
            timestamp=datetime.utcnow(),
            model_name="LSTM-v1",
            model_version="1.0.0",
            prediction_type="Buy/Sell",
            features_used={"sequence_mean": float(sum(features)/len(features))},  # placeholder
            source_model_version="lstm_model.pth"
        )
    except Exception as e:
        logging.error(f"Inference failed: {e}")
        return _fallback_response(ticker, reason="inference_error")

# ----------------------
# Fallback Response
# ----------------------
def _fallback_response(ticker: str, reason: str = "error") -> Dict:
    return {
        "ticker": ticker,
        "prediction": 0,
        "confidence": 0.5,
        "confidence_band": {"lower": 0.45, "upper": 0.55},
        "rationale": f"Fallback response due to {reason}",
        "timestamp": datetime.utcnow(),
        "model_name": "LSTM-v1",
        "model_version": "1.0.0",
        "prediction_type": "Buy/Sell",
        "features_used": {},
        "source_model_version": "lstm_model.pth"
    }



