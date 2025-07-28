from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


# ----- User Schemas -----

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# ----- Prediction Schemas -----

class PredictionBase(BaseModel):
    symbol: str
    model_name: str
    prediction: int
    confidence: float


class PredictionCreate(PredictionBase):
    user_id: int


class Prediction(PredictionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


# ----- Training Schemas -----

class TrainingLogBase(BaseModel):
    model_name: str
    accuracy: float
    loss: float
    duration_seconds: float


class TrainingLogCreate(TrainingLogBase):
    user_id: int


class TrainingLog(TrainingLogBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
