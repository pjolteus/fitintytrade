import pytest
from unittest.mock import patch, MagicMock
from tasks.train import train_model_task
from services import system_monitor

# ----------------------------
# Test: Successful Training Flow
# ----------------------------
@patch("train.trainer.train_model")
@patch("train.utils.evaluate_model")
@patch("db.connection.SessionLocal")
@patch("services.system_monitor.log_model_metadata")
@patch("services.system_monitor.log_task_duration")
def test_train_model_success(mock_duration, mock_metadata, mock_session, mock_evaluate, mock_train):
    # Mock training result
    mock_train.return_value = {"model_version": "v1.2.3"}
    mock_evaluate.return_value = {"accuracy": 0.92, "f1_score": 0.91, "loss": 0.08}

    # Mock DB session
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    # Run task
    train_model_task(model_type="lstm")

    # Check Redis logging
    mock_metadata.assert_called_with(version="v1.2.3", task_id=ANY, accuracy=0.92, f1=0.91)
    mock_duration.assert_called()
    mock_db.add.assert_called()
    mock_db.commit.assert_called()
    mock_db.close.assert_called()


# ----------------------------
# Test: Failed Training Flow
# ----------------------------
@patch("train.trainer.train_model", side_effect=Exception("Simulated training error"))
@patch("db.connection.SessionLocal")
@patch("services.system_monitor.log_task_failure")
def test_train_model_failure(mock_failure_log, mock_session, mock_train):
    # Mock DB session
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    with pytest.raises(Exception) as exc_info:
        train_model_task(model_type="lstm")

    assert "Simulated training error" in str(exc_info.value)
    mock_failure_log.assert_called()
    mock_db.rollback.assert_called()
    mock_db.close.assert_called()
