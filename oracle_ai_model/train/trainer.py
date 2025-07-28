# oracle_ai_model/train/trainer.py

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
import numpy as np
import os
from datetime import datetime

from oracle_ai_model.utils.helpers import add_technical_indicators, normalize
from oracle_ai_model.data.loader import download_stock_data
from oracle_ai_model.models.model import LSTMModel
from oracle_ai_model.models.gru_model import GRUTimeSeriesModel
from oracle_ai_model.models.tcn_model import TCN
from oracle_ai_model.models.transformer_model import TransformerTimeSeriesModel
from oracle_ai_model.train.config import TRAINING_CONFIG


def prepare_sequences(df, seq_length):
    data = df[TRAINING_CONFIG["features"]].values
    sequences, labels = [], []
    for i in range(len(data) - seq_length - 1):
        sequences.append(data[i:i+seq_length])
        labels.append(1 if data[i+seq_length][0] > data[i+seq_length-1][0] else 0)
    return np.array(sequences), np.array(labels)


def select_model(input_size):
    model_type = TRAINING_CONFIG["model_type"]
    if model_type == "lstm":
        return LSTMModel(input_size)
    elif model_type == "gru":
        return GRUTimeSeriesModel(input_size)
    elif model_type == "tcn":
        return TCN(input_size, TRAINING_CONFIG["tcn_channels"])
    elif model_type == "transformer":
        return TransformerTimeSeriesModel(input_size)
    else:
        raise ValueError("Unsupported model type")


def train():
    df = download_stock_data(TRAINING_CONFIG["symbol"], period="1mo")
    df = add_technical_indicators(df)
    df = normalize(df, TRAINING_CONFIG["features"])

    X, y = prepare_sequences(df, TRAINING_CONFIG["seq_length"])
    dataset = TensorDataset(torch.tensor(X).float(), torch.tensor(y).float())

    val_size = int(len(dataset) * TRAINING_CONFIG["validation_split"])
    train_size = len(dataset) - val_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=TRAINING_CONFIG["batch_size"], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=TRAINING_CONFIG["batch_size"])

    model = select_model(X.shape[2])
    device = torch.device("cuda" if TRAINING_CONFIG["use_cuda"] and torch.cuda.is_available() else "cpu")
    model.to(device)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=TRAINING_CONFIG["learning_rate"])

    best_loss = float('inf')
    patience = TRAINING_CONFIG["early_stopping_patience"]
    patience_counter = 0
    save_path = os.path.join(TRAINING_CONFIG["save_dir"], f"{TRAINING_CONFIG["model_type"]}_{TRAINING_CONFIG["timestamp"]}.pth")

    for epoch in range(TRAINING_CONFIG["epochs"]):
        model.train()
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            optimizer.zero_grad()
            output = model(batch_X).squeeze()
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()

        # Validation loss
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for val_X, val_y in val_loader:
                val_X, val_y = val_X.to(device), val_y.to(device)
                val_output = model(val_X).squeeze()
                val_loss += criterion(val_output, val_y).item()

        val_loss /= len(val_loader)
        print(f"Epoch {epoch+1}, Validation Loss: {val_loss:.4f}")

        if val_loss < best_loss:
            best_loss = val_loss
            patience_counter = 0
            torch.save(model.state_dict(), save_path)
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print("Early stopping triggered.")
                break

    print(f"Training complete. Model saved to {save_path}")
