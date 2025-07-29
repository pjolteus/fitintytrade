from pydantic import BaseModel

class TrainRequest(BaseModel):
    model_type: str
    data_source: str
    hyperparameters: dict

class TrainResponse(BaseModel):
    status: str
    message: str

