import redis
import json
import time
from config import settings

r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

# -------------------------
# 🔁 Training Metadata
# -------------------------
def log_model_metadata(version: str, task_id: str, accuracy: float, f1: float = None):
    metadata = {
        "model_version": version,
        "last_task_id": task_id,
        "accuracy": accuracy,
        "f1_score": f1 or "n/a",
        "last_trained": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    r.hset("fitinty:meta", mapping=metadata)


# -------------------------
# 🔎 Prediction Log (per user)
# -------------------------
def log_last_prediction(user_id: str, symbol: str, confidence: float, prediction: int):
    key = f"fitinty:last_prediction:{user_id}"
    value = {
        "symbol": symbol,
        "confidence": confidence,
        "prediction": prediction,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    r.set(key, json.dumps(value))


# -------------------------
# 🧠 Task Failure Reporting
# -------------------------
def log_task_failure(task_name: str, error: str):
    r.lpush("fitinty:task_errors", json.dumps({
        "task": task_name,
        "error": error,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }))
    r.ltrim("fitinty:task_errors", 0, 49)  # keep only last 50


# -------------------------
# ⏱️ Duration Tracker
# -------------------------
def log_task_duration(task_name: str, start: float, end: float):
    r.hset("fitinty:durations", task_name, f"{end - start:.2f} seconds")


# -------------------------
# 📊 Status Snapshot
# -------------------------
def get_system_status():
    return {
        "meta": r.hgetall("fitinty:meta"),
        "durations": r.hgetall("fitinty:durations"),
        "recent_errors": [json.loads(e) for e in r.lrange("fitinty:task_errors", 0, 4)]
    }


