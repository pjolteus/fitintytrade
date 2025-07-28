import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging(service_name="backend"):
    log_file = os.path.join(LOG_DIR, f"{service_name}.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
    handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(stream_handler)
