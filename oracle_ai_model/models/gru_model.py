# models/gru_model.py
import torch
import torch.nn as nn
from .model import BaseModel

class GRUTimeSeriesModel(BaseModel):
    def __init__(self, input_size, hidden_size=64, output_size=1, num_layers=2, dropout=0.2):
        super().__init__()
        self.gru = nn.GRU(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(dropout)
        self.output_size = output_size

    def forward(self, x):
        self.validate_input(x)
        out, _ = self.gru(x)
        out = out.mean(dim=1)  # mean pooling
        out = self.dropout(out)
        return self.fc(out)

    def __repr__(self):
        return f"GRUTimeSeriesModel(input_size={self.gru.input_size}, hidden_size={self.gru.hidden_size}, output_size={self.output_size})"
