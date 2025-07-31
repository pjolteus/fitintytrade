# backend_api/tasks/fetch_task.py

from celery import shared_task
from oracle_ai_model.data.fetch_enrich_save import fetch_enrich_and_save

@shared_task
def fetch_and_store_market_data(symbol: str):
    try:
        df = fetch_enrich_and_save(symbol)
        return {"status": "success", "rows": len(df)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
