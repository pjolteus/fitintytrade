import json
import os
from datetime import datetime


def save_metrics_to_json(metrics: dict, model_name: str, output_dir="logs"):
    """
    Save metrics dictionary to a timestamped JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{model_name}_metrics_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"[Logger] Metrics saved to {filepath}")
    return filepath


def append_log_entry(message: str, log_file="logs/evaluation_log.txt"):
    """
    Append a simple log entry to a flat text file.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[Logger] Logged: {message}")
