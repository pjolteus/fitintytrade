# oracle_ai_model/train/train_model.py

import torch
import torch.nn as nn
import torch.optim as optim
import os
import matplotlib.pyplot as plt
from datetime import datetime
from oracle_ai_model.utils.helpers import add_technical_indicators, normalize
from oracle_ai_model.data.loader import download_stock_data
from oracle_ai_model.train.utils import prepare_sequences, create_dataloaders, get_device, evaluate_model
from oracle_ai_model.train.config import TRAINING_CONFIG

# Dynamic model loader
def load_model_class(model_type, input_size):
    if model_type == "lstm":
        from oracle_ai_model.models.model import LSTMModel
        return LSTMModel(input_size)
    elif model_type == "gru":
        from oracle_ai_model.models.gru_model import GRUTimeSeriesModel
        return GRUTimeSeriesModel(input_size)
    elif model_type == "transformer":
        from oracle_ai_model.models.transformer_model import TransformerTimeSeriesModel
        return TransformerTimeSeriesModel(input_size)
    elif model_type == "tcn":
        from oracle_ai_model.models.tcn_model import TCN
        return TCN(input_size=input_size, num_channels=TRAINING_CONFIG["tcn_channels"])
    else:
        raise ValueError("Unsupported model type")

def plot_loss_curve(train_losses, val_losses, save_path):
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Val Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Training Curve')
    plt.savefig(save_path)
    plt.close()

def train():
    cfg = TRAINING_CONFIG
    df = download_stock_data(cfg["symbol"], period="1mo")
    df = add_technical_indicators(df)
    df = normalize(df, cfg["features"])
    
    X, y = prepare_sequences(df, cfg["features"], cfg["seq_length"])
    train_loader, val_loader = create_dataloaders(X, y, cfg["batch_size"], cfg["validation_split"])

    device = get_device(cfg["use_cuda"])
    model = load_model_class(cfg["model_type"], input_size=X.shape[2]).to(device)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=cfg["learning_rate"])

    best_val_loss = float('inf')
    patience_counter = 0
    train_losses, val_losses = [], []

    for epoch in range(cfg["epochs"]):
        model.train()
        epoch_loss = 0
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            optimizer.zero_grad()
            output = model(batch_X).squeeze()
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        train_loss = epoch_loss / len(train_loader)
        val_loss, val_acc = evaluate_model(model, val_loader, criterion, device)

        train_losses.append(train_loss)
        val_losses.append(val_loss)

        print(f"Epoch {epoch+1}: Train Loss = {train_loss:.4f}, Val Loss = {val_loss:.4f}, Val Acc = {val_acc:.2f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            save_path = os.path.join(cfg["save_dir"], f"{cfg['model_type']}_model_{cfg['timestamp']}.pth")
            torch.save(model.state_dict(), save_path)
            print(f"✅ Saved best model to {save_path}")
        else:
            patience_counter += 1
            if patience_counter >= cfg["early_stopping_patience"]:
                print("⏹️ Early stopping triggered.")
                break

    plot_path = os.path.join(cfg["save_dir"], f"loss_curve_{cfg['timestamp']}.png")
    plot_loss_curve(train_losses, val_losses, plot_path)
    print(f"📈 Training curve saved to {plot_path}")

if __name__ == "__main__":
    train()
