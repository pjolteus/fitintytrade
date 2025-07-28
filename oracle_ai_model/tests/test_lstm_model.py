import torch
import torch.nn as nn

# Minimal LSTMModel definition
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size=32, output_size=1, num_layers=1, dropout=0.1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        if len(x.shape) != 3:
            raise ValueError("Input must be 3D tensor: (batch, seq_len, features)")
        out, _ = self.lstm(x)
        out = out.mean(dim=1)
        out = self.dropout(out)
        return self.fc(out)

# Safe input for small systems
BATCH_SIZE = 2
SEQ_LEN = 5
INPUT_FEATURES = 4

def main():
    print("Initializing LSTMModel...")
    model = LSTMModel(input_size=INPUT_FEATURES)
    dummy_input = torch.randn(BATCH_SIZE, SEQ_LEN, INPUT_FEATURES)
    print("Running forward pass...")
    output = model(dummy_input)
    print("✅ Model output:", output)
    print("✅ Output shape:", output.shape)

if __name__ == "__main__":
    main()
