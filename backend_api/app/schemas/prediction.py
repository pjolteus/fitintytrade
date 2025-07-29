from pydantic import BaseModel

class PredictionInput(BaseModel):
    ticker: str
    model: str

class PredictionOutput(BaseModel):
    prediction: int
    confidence: float
