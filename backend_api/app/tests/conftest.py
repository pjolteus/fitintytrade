# tests/conftest.py
import pytest
import redis
from config import settings

@pytest.fixture(scope="session")
def redis_conn():
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

@pytest.fixture(autouse=True)
def clean_redis(redis_conn):
    # Clean Redis state before and after each test
    keys_to_delete = ["fitinty:meta", "fitinty:durations", "fitinty:task_errors"]
    for key in keys_to_delete:
        redis_conn.delete(key)
    for key in redis_conn.keys("fitinty:last_prediction:*"):
        redis_conn.delete(key)
    yield
    for key in keys_to_delete:
        redis_conn.delete(key)
    for key in redis_conn.keys("fitinty:last_prediction:*"):
        redis_conn.delete(key)

