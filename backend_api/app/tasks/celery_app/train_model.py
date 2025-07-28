
from celery import Celery

celery_app = Celery(
    "fitinty_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

@celery_app.task
def train_model_task():
    from app.tasks.tasks import background_train_model
    return background_train_model()
