# backend_api/api/daily_signals.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/daily-signals")
def get_top10_signals():
    return {
        "calls": [
            {"symbol": "AAPL", "confidence": 0.92},
            {"symbol": "TSLA", "confidence": 0.89},
            # ...
        ],
        "puts": [
            {"symbol": "EURUSD", "confidence": 0.91},
            {"symbol": "NFLX", "confidence": 0.87},
            # ...
        ]
    }
