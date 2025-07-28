# models/model.py
import torch
import torch.nn as nn
from .lstm_model import LSTMModel
from .gru_model import GRUTimeSeriesModel
from .tcn_model import TCN
from .transformer_model import TransformerTimeSeriesModel

class ModelRegistry:
    def __init__(self):
        self.models = {
            "lstm": lambda **kwargs: LSTMModel(**kwargs),
            "gru": lambda **kwargs: GRUTimeSeriesModel(**kwargs),
            "tcn": lambda **kwargs: TCN(input_size=kwargs['input_size'], num_channels=[32, 64]),
            "transformer": lambda **kwargs: TransformerTimeSeriesModel(**kwargs)
        }

    def get_model(self, model_type: str, **kwargs):
        if model_type not in self.models:
            raise ValueError(f"Model '{model_type}' not supported. Available: {list(self.models.keys())}")
        return self.models[model_type](**kwargs)

def load_model(model_type: str, model_path: str, **kwargs):
    model = ModelRegistry().get_model(model_type, **kwargs)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

# Optional BaseModel for interface compliance (future enhancement)
class BaseModel(nn.Module):
    def __init__(self):
        super(BaseModel, self).__init__()

    def forward(self, x):
        raise NotImplementedError("Subclasses should implement this method")

    def validate_input(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        if len(x.shape) != 3:
            raise ValueError("Input must be 3D tensor: (batch, seq_len, features)")

    def __repr__(self):
        return f"{self.__class__.__name__} with {sum(p.numel() for p in self.parameters())} parameters"

# Example usage in training/inference
if __name__ == "__main__":
    model = ModelRegistry().get_model("lstm", input_size=5)
    print(model)
