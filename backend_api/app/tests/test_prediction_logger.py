import json
import redis
import pytest
import time

from prediction_logger import (
    log_prediction,
    get_last_prediction,
    clear_all_predictions,
    log_model_metadata,
    log_task_failure,
    log_task_duration,
    get_system_status
)
from config import settings

r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


@pytest.fixture(autouse=True)
def clear_before_and_after():
    # Cleanup all known keys before and after tests
    r.delete("fitinty:meta")
    r.delete("fitinty:durations")
    r.delete("fitinty:task_errors")
    for key in r.keys("fitinty:last_prediction:*"):
        r.delete(key)
    yield
    r.delete("fitinty:meta")
    r.delete("fitinty:durations")
    r.delete("fitinty:task_errors")
    for key in r.keys("fitinty:last_prediction:*"):
        r.delete(key)


def test_log_and_get_prediction():
    user_id = "testuser"
    symbol = "BTCUSD"
    confidence = 0.92
    prediction = 1

    log_prediction(user_id, symbol, confidence, prediction)
    result = get_last_prediction(user_id)

    assert result is not None
    assert result["symbol"] == symbol
    assert result["confidence"] == confidence
    assert result["prediction"] == prediction
    assert "timestamp" in result


def test_get_last_prediction_none():
    assert get_last_prediction("ghost_user") is None


def test_clear_all_predictions():
    log_prediction("u1", "ETHUSD", 0.88, 0)
    log_prediction("u2", "BTCUSD", 0.91, 1)

    assert len(r.keys("fitinty:last_prediction:*")) == 2
    clear_all_predictions()
    assert len(r.keys("fitinty:last_prediction:*")) == 0


def test_log_model_metadata():
    log_model_metadata("v1.0.0", "task123", accuracy=0.95, f1=0.88)
    meta = r.hgetall("fitinty:meta")

    assert meta["model_version"] == "v1.0.0"
    assert meta["last_task_id"] == "task123"
    assert float(meta["accuracy"]) == 0.95
    assert float(meta["f1_score"]) == 0.88
    assert "last_trained" in meta


def test_log_task_failure():
    log_task_failure("daily_crypto_autotrade", "Exchange timeout")
    errors = r.lrange("fitinty:task_errors", 0, -1)

    assert len(errors) > 0
    data = json.loads(errors[0])
    assert data["task"] == "daily_crypto_autotrade"
    assert data["error"] == "Exchange timeout"
    assert "timestamp" in data


def test_log_task_duration():
    task_name = "train_model_task"
    start = time.time()
    time.sleep(0.01)
    end = time.time()

    log_task_duration(task_name, start, end)
    duration_str = r.hget("fitinty:durations", task_name)

    assert duration_str is not None
    assert "seconds" in duration_str


def test_get_system_status_summary():
    log_model_metadata("v2.1.0", "abc", 0.91)
    log_task_failure("run_auto_crypto_trading", "price fetch error")
    log_task_duration("train", time.time(), time.time() + 0.1)

    status = get_system_status()

    assert "meta" in status
    assert "durations" in status
    assert "recent_errors" in status
    assert isinstance(status["recent_errors"], list)
    assert "model_version" in status["meta"]
    assert "train" in status["durations"]
