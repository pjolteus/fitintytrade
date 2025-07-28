# oracle_ai_model/train/utils.py

import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, random_split
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def prepare_sequences(df, features, seq_length=24):
    data = df[features].values
    sequences, labels = [], []
    for i in range(len(data) - seq_length - 1):
        sequences.append(data[i:i+seq_length])
        labels.append(1 if data[i+seq_length][0] > data[i+seq_length-1][0] else 0)
    X, y = np.array(sequences), np.array(labels)
    return X, y

def create_dataloaders(X, y, batch_size, validation_split=0.2):
    X_tensor = torch.tensor(X).float()
    y_tensor = torch.tensor(y).float()
    dataset = TensorDataset(X_tensor, y_tensor)

    val_size = int(len(dataset) * validation_split)
    train_size = len(dataset) - val_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader

def get_device(use_cuda=True):
    return torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")

def evaluate_model(model, val_loader, criterion, device):
    model.eval()
    val_loss = 0
    preds, trues = [], []

    with torch.no_grad():
        for X_batch, y_batch in val_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            output = model(X_batch).squeeze()
            loss = criterion(output, y_batch)
            val_loss += loss.item()
            preds.extend(torch.sigmoid(output).round().cpu().numpy())
            trues.extend(y_batch.cpu().numpy())

    acc = accuracy_score(trues, preds)
    avg_loss = val_loss / len(val_loader)
    return avg_loss, acc
