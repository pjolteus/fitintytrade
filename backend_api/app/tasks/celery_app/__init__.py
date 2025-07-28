from celery import Celery
from celery.schedules import crontab
from celery.signals import task_failure, task_postrun, task_prerun
from config.env_settings import settings
import logging
import smtplib
from email.message import EmailMessage
import os

# --------------------------
# Celery App Initialization
# --------------------------
celery_app = Celery(
    "fitintytrade_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["tasks.train", "tasks.crypto_daily_job"]
)

celery_app.conf.beat_schedule = {
    "periodic_model_training": {
        "task": "tasks.train.train_model_task",
        "schedule": crontab(minute=0, hour="*/12"),
    },
    "daily_crypto_autotrade": {
        "task": "tasks.crypto_daily_job.run_auto_crypto_trading",
        "schedule": crontab(minute=0, hour=3),
    }
}

celery_app.conf.timezone = "UTC"

# --------------------------
# Debugging & Reliability Settings
# --------------------------
celery_app.conf.update(
    task_track_started=True,
    task_time_limit=1800,               # 30 minutes
    worker_max_tasks_per_child=50,      # Recycle to prevent memory leaks
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# --------------------------
# Logging
# --------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@task_prerun.connect
def task_start_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **extra):
    logging.info(f"🚀 Task started: {sender.name} (id={task_id})")

@task_postrun.connect
def task_complete_handler(sender=None, task_id=None, retval=None, **kwargs):
    logging.info(f"✅ Task completed: {sender.name} (id={task_id})")

# --------------------------
# Email Notification on Failure
# --------------------------
@task_failure.connect
def task_failed_handler(sender=None, task_id=None, exception=None, traceback=None, **kwargs):
    subject = f"🚨 Celery Task Failed: {sender.name}"
    body = f"""
    Task ID: {task_id}
    Task Name: {sender.name}
    Error: {exception}
    """

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = settings.DEV_EMAIL
        msg.set_content(body)

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
            smtp.send_message(msg)
        logging.error(f"📧 Sent failure alert email for task {sender.name}")
    except Exception as email_error:
        logging.error(f"❌ Failed to send email alert: {email_error}")

# --------------------------
# Pytest Loader for CI/CD
# --------------------------
def run_tests():
    """
    Helper to auto-run all tests in the /tests folder during CI/CD or local QA.
    Example:
        from tasks import run_tests
        run_tests()
    """
    import subprocess
    test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
    logging.info(f"🧪 Running tests from: {test_dir}")
    result = subprocess.run(["pytest", test_dir])
    if result.returncode != 0:
        raise SystemExit(f"❌ Tests failed with code {result.returncode}")
    else:
        logging.info("✅ All tests passed.")
