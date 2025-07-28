
import torch
import torch.nn as nn
from models.model import BaseModel

class TransformerTimeSeriesModel(BaseModel):
    def __init__(
        self,
        input_size=6,
        d_model=64,
        nhead=4,
        num_layers=2,
        output_size=1,
        dropout=0.1
    ):
        super(TransformerTimeSeriesModel, self).__init__()
        self.model_type = 'Transformer'
        self.input_size = input_size
        self.output_size = output_size

        self.embedding = nn.Linear(input_size, d_model)
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        encoder_layers = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dropout=dropout)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers=num_layers)
        self.decoder = nn.Linear(d_model, output_size)
        self.sigmoid = nn.Sigmoid()

    def validate_input(self, x):
        if x.dim() != 3 or x.size(2) != self.input_size:
            raise ValueError(f"Expected input shape (batch, seq_len, {self.input_size}), got {x.shape}")

    def forward(self, src):
        self.validate_input(src)
        src = self.embedding(src)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src)
        pooled = torch.mean(output, dim=1)  # Mean pooling instead of using only last timestep
        output = self.decoder(pooled)
        return self.sigmoid(output)

    def __repr__(self):
        return f"{self.__class__.__name__}(input_size={self.input_size}, output_size={self.output_size})"

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=500):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model).float()
        position = torch.arange(0, max_len).float().unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-torch.log(torch.tensor(10000.0)) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        if d_model % 2 == 1:
            pe[:, 1::2] = torch.cos(position * div_term[:-1])
        else:
            pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return self.dropout(x)
