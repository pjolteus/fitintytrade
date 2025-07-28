import pytest
import redis
import json
from system_monitor import (
    log_model_metadata,
    log_last_prediction,
    get_system_status
)
from config import settings

# Use the same Redis client for validation
r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

@pytest.fixture(autouse=True)
def clear_before_and_after():
    r.delete("fitinty:meta")
    r.delete("fitinty:last_prediction:testuser")
    yield
    r.delete("fitinty:meta")
    r.delete("fitinty:last_prediction:testuser")


def test_log_model_metadata():
    log_model_metadata(version="1.2.3", task_id="abc123", accuracy=0.95)
    metadata = r.hgetall("fitinty:meta")

    assert metadata["model_version"] == "1.2.3"
    assert metadata["last_task_id"] == "abc123"
    assert float(metadata["accuracy"]) == 0.95


def test_log_last_prediction():
    log_last_prediction(user_id="testuser", symbol="BTCUSD", confidence=0.87)
    result = r.get("fitinty:last_prediction:testuser")

    assert result is not None
    data = json.loads(result)
    assert data["symbol"] == "BTCUSD"
    assert data["confidence"] == 0.87


def test_get_system_status_after_logging():
    log_model_metadata(version="0.9.1", task_id="xyz789", accuracy=0.88)
    status = get_system_status()

    assert "model_version" in status
    assert status["model_version"] == "0.9.1"
    assert "accuracy" in status
    assert float(status["accuracy"]) == 0.88
