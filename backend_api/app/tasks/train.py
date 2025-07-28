import time
import logging
from datetime import datetime
from celery_app import celery_app
from db.connection import SessionLocal
from db.models.training_log import TrainingLog
from train.trainer import train_model  # core training logic
from train.utils import evaluate_model  # returns evaluation metrics
from services.system_monitor import (
    log_model_metadata,
    log_task_duration,
    log_task_failure
)

@celery_app.task(name="tasks.train.train_model_task", bind=True, max_retries=3)
def train_model_task(self, model_type="lstm"):
    start_time = time.time()
    db = SessionLocal()

    try:
        logging.info(f"🧠 Starting model training for: {model_type}")

        # Train the model (returns model_version, etc.)
        metrics = train_model(model_type)

        # Evaluate the trained model
        evaluation = evaluate_model(model_type)
        acc = evaluation.get("accuracy")
        f1 = evaluation.get("f1_score")
        loss = evaluation.get("loss")
        version = metrics.get("model_version", "v1.0.0")

        # Persist training metadata to DB
        log = TrainingLog(
            model_type=model_type,
            started_at=datetime.utcnow(),
            duration=time.time() - start_time,
            accuracy=acc,
            f1_score=f1,
            loss=loss,
            model_version=version
        )
        db.add(log)
        db.commit()

        logging.info(f"✅ Training complete for {model_type} in {log.duration:.2f}s")

        # Log to Redis
        log_model_metadata(version=version, task_id=str(self.request.id), accuracy=acc, f1=f1)
        log_task_duration("train_model_task", start_time, time.time())

    except Exception as e:
        db.rollback()
        logging.error(f"❌ Training failed: {e}")
        log_task_failure("train_model_task", str(e))
        raise self.retry(exc=e, countdown=30)

    finally:
        db.close()
