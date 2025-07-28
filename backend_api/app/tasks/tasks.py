
from datetime import datetime
import time

def background_train_model():
    print(f"[{datetime.utcnow()}] Starting background model training...")
    time.sleep(5)
    print(f"[{datetime.utcnow()}] Model training completed.")
    return "Background training finished."
