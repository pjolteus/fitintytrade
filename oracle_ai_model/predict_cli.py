# oracle_ai_model/predict_cli.py

import argparse
from predict_from_model import run_prediction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run prediction for a symbol using a specified model.")
    parser.add_argument("symbol", type=str, help="Ticker symbol (e.g., AAPL)")
    parser.add_argument("--model", type=str, default="lstm", help="Model type: lstm, gru, tcn, transformer")
    
    args = parser.parse_args()
    
    result = run_prediction(args.symbol, args.model)
    print(result)
