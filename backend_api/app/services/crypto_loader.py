# services/crypto_loader.py

import requests

def get_top_crypto_symbols(limit=50):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    response = requests.get(url, params={
        "vs_currency": "usd",
        "order": "volume_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false"
    })

    data = response.json()
    return [item["symbol"].upper() + "USDT" for item in data if item.get("symbol")]
