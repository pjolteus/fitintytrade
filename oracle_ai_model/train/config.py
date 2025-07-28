# oracle_ai_model/train/config.py

from datetime import datetime

TRAINING_CONFIG = {
    # Data settings
    "symbol": "AAPL",
    "seq_length": 24,
    "validation_split": 0.2,

    # Model type: "lstm", "gru", "transformer", "tcn"
    "model_type": "lstm",  # default; can be overridden by Optuna

    # Training hyperparameters
    "batch_size": 32,
    "epochs": 20,
    "learning_rate": 0.001,
    "early_stopping_patience": 3,

    # Optuna tuning
    "use_optuna": True,
    "optuna_trials": 30,

    # Save settings
    "save_dir": "models/",
    "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),

    # Input features to normalize
    "features": ["Close", "rsi", "macd", "ema", "volatility"],

    # Channels for TCN if needed
    "tcn_channels": [32, 64],

    # GPU support (if available)
    "use_cuda": True
}
