import requests

BASE_URL = "https://data.binance.vision"

def fetch_historical_candles(symbol: str, interval: str, limit: int = 100):
    url = f"https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            # fallback automático
            url_alt = "https://api.binance.us/api/v3/klines"
            response = requests.get(url_alt, params=params, timeout=10)

        response.raise_for_status()

        data = response.json()

        return [
            {
                "time": int(k[0] / 1000),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
            }
            for k in data
        ]

    except Exception as e:
        raise Exception(f"binance_fetch_failed: {str(e)}")
