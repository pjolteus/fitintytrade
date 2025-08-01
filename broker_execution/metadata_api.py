# 📂 File: backend_api/broker_execution/metadata_api.py
from fastapi import APIRouter
from broker_execution.broker_metadata import BROKER_METADATA

router = APIRouter()

@router.get("/broker-info")
def get_broker_info():
    return BROKER_METADATA
