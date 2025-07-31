# backend_api/app/api/routes/market.py

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from backend_api.app.db.connection import SessionLocal
from backend_api.app.db.models import MarketSnapshotLog
from backend_api.app.dependencies.auth import get_current_admin_user  # Ensure this exists

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Filter + Pagination + Admin Auth
@router.get("/market-logs", dependencies=[Depends(get_current_admin_user)])
async def get_market_logs(
    db: Session = Depends(get_db),
    symbol: str = Query(None, description="Filter by symbol (e.g. AAPL)"),
    status: str = Query(None, description="Filter by status (e.g. success, failed)"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    try:
        query = db.query(MarketSnapshotLog)

        if symbol:
            query = query.filter(MarketSnapshotLog.symbol.ilike(f"%{symbol}%"))
        if status:
            query = query.filter(MarketSnapshotLog.status.ilike(f"%{status}%"))

        logs = query.order_by(MarketSnapshotLog.timestamp.desc()).offset(offset).limit(limit).all()

        return [
            {
                "id": log.id,
                "symbol": log.symbol,
                "status": log.status,
                "message": log.message,
                "row_count": log.row_count,
                "timestamp": log.timestamp.isoformat(),
            }
            for log in logs
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
