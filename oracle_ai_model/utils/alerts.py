from db.connection import SessionLocal
from db.models.alert_log import AlertLog

def send_alert(message: str, type: str = "INFO", symbol: str = "N/A"):
    if SLACK_WEBHOOK_URL:
        try:
            requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        except Exception as e:
            print(f"Slack alert failed: {e}")
    
    # Also log in DB
    try:
        db = SessionLocal()
        alert = AlertLog(type=type, symbol=symbol, message=message)
        db.add(alert)
        db.commit()
        db.close()
    except Exception as e:
        print(f"[DB] Failed to log alert: {e}")

