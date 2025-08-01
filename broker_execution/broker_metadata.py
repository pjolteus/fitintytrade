# 📂 File: backend_api/broker_execution/broker_metadata.py

BROKER_METADATA = {
    "alpaca": {
        "max_leverage": 2,
        "margin_required": 0.5,
        "commission": 0.0,
        "asset_types": ["stocks", "ETFs"]
    },
    "oanda": {
        "max_leverage": 50,
        "margin_required": 0.02,
        "commission": 0.0,
        "asset_types": ["forex", "commodities"]
    },
    "ibr": {
        "max_leverage": 30,
        "margin_required": 0.033,
        "commission": 1.0,
        "asset_types": ["stocks", "options", "futures", "forex"]
    },
    "fxcm": {
        "max_leverage": 400,
        "margin_required": 0.0025,
        "commission": 0.0,
        "asset_types": ["forex", "CFDs"]
    },
    "bybit": {
        "max_leverage": 100,
        "margin_required": 0.01,
        "commission": 0.075,
        "asset_types": ["crypto"]
    },
    "binance": {
        "max_leverage": 125,
        "margin_required": 0.008,
        "commission": 0.1,
        "asset_types": ["crypto"]
    },
    "coinbase": {
        "max_leverage": 3,
        "margin_required": 0.33,
        "commission": 1.5,
        "asset_types": ["crypto"]
    }
}
