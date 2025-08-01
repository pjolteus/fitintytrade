# broker_execution/broker_config.py

def get_broker_params(broker: str, symbol: str) -> dict:
    broker = broker.lower()
    mapping = {
        "alpaca": {
            "leverage": 2,
            "margin_requirement": 0.5,
            "commission": 0.0,
            "fee_per_trade": 0.01,
            "spread": 0.02
        },
        "oanda": {
            "leverage": 20,
            "margin_requirement": 0.05,
            "commission": 0.0,
            "fee_per_trade": 0.0,
            "spread": 0.0003
        },
        "fxcm": {
            "leverage": 50,
            "margin_requirement": 0.02,
            "commission": 0.0,
            "fee_per_trade": 0.0,
            "spread": 0.0001
        },
        "interactive_brokers": {
            "leverage": 4,
            "margin_requirement": 0.25,
            "commission": 0.005,
            "fee_per_trade": 1.0,
            "spread": 0.01
        },
    }
    return mapping.get(broker, {
        "leverage": 1,
        "margin_requirement": 1,
        "commission": 0,
        "fee_per_trade": 0,
        "spread": 0
    })
