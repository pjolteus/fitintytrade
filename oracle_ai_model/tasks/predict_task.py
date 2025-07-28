# backend_api/tasks/predict_task.py

from celery import shared_task
from oracle_ai_model.predict_from_model import run_prediction

@shared_task
def async_predict(symbol: str, model_type: str = "lstm"):
    return run_prediction(symbol, model_type)
