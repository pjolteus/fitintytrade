import torch
import numpy as np
import pandas as pd

from oracle_ai_model.models.model import LSTMModel
from oracle_ai_model.models.gru_model import GRUTimeSeriesModel
from oracle_ai_model.models.tcn_model import TCN
from oracle_ai_model.models.transformer_model import TransformerTimeSeriesModel

from oracle_ai_model.utils.helpers import add_technical_indicators, normalize
from oracle_ai_model.data.loader import download_stock_data


def prepare_input_sequence(df: pd.DataFrame, seq_length: int = 24):
    data = df[["Close", "rsi", "macd", "ema", "volatility"]].values
    sequence = np.expand_dims(data[-seq_length:], axis=0)  # Shape: (1, seq_len, features)
    return torch.tensor(sequence).float()


def get_model_instance(model_type: str, input_size: int):
    if model_type == "lstm":
        return LSTMModel(input_size)
    elif model_type == "gru":
        return GRUTimeSeriesModel(input_size)
    elif model_type == "tcn":
        return TCN(input_size=input_size, num_channels=[32, 64])
    elif model_type == "transformer":
        return TransformerTimeSeriesModel(input_size)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")


def predict_from_model(symbol: str, model_type: str = "lstm", model_path: str = None):
    try:
        symbol = symbol.upper()
        df = download_stock_data(symbol, period="1mo")
        df = add_technical_indicators(df)
        df = normalize(df, ["Close", "rsi", "macd", "ema", "volatility"])

        input_tensor = prepare_input_sequence(df)
        input_size = input_tensor.shape[2]

        if not model_path:
            model_path = f"{model_type}_model.pth"

        model = get_model_instance(model_type, input_size)
        model.load_state_dict(torch.load(model_path))
        model.eval()

        with torch.no_grad():
            output = model(input_tensor)
            prob = torch.sigmoid(output).item()
            prediction = int(prob > 0.5)

        return {
            "symbol": symbol,
            "model_type": model_type,
            "prediction": prediction,
            "confidence": prob
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
