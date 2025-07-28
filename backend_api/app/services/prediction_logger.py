import redis
import json
import time
from config import settings

# Connect to Redis
r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

# -------------------------
# 🔎 Prediction Log (per user)
# -------------------------
def log_prediction(user_id: str, symbol: str, confidence: float, prediction: int):
    """
    Stores the last prediction result for the user.
    """
    key = f"fitinty:last_prediction:{user_id}"
    payload = {
        "symbol": symbol,
        "confidence": confidence,
        "prediction": prediction,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    r.set(key, json.dumps(payload))


# -------------------------
# 📖 Retrieve Last Prediction
# -------------------------
def get_last_prediction(user_id: str):
    """
    Retrieves the last prediction made for the user, if available.
    """
    key = f"fitinty:last_prediction:{user_id}"
    raw = r.get(key)
    return json.loads(raw) if raw else None


# -------------------------
# 🧹 Clear Prediction Logs (Admin Use)
# -------------------------
def clear_all_predictions():
    """
    (Admin use) Clears all last prediction keys.
    WARNING: Use with caution in production.
    """
    keys = r.keys("fitinty:last_prediction:*")
    if keys:
        r.delete(*keys)
