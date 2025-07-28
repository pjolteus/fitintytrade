from deploy.monitoring.logging_config import setup_logging
setup_logging("worker")

from celery.schedules import crontab

beat_schedule = {
    "auto-close-positions-AM": {
        "task": "tasks.auto_close.auto_close_positions_task",
        "schedule": crontab(hour=9, minute=29),  # 1 min before open
    },
    "auto-close-positions-PM": {
        "task": "tasks.auto_close.auto_close_positions_task",
        "schedule": crontab(hour=15, minute=59),  # 1 min before close
    },
}

