import requests

from .config import (
    ALLOWED_INTERVALS,
    BINANCE_REST_BASE,
    DEFAULT_LIMIT,
    DEFAULT_SYMBOL,
    KLINES_ENDPOINT,
)
from .schemas import Candle, HistoricalCandlesResponse


def validate_interval(interval: str) -> str:
    interval = interval.strip()
    if interval not in ALLOWED_INTERVALS:
        raise ValueError(
            f"Intervalo no permitido: {interval}. "
            f"Permitidos: {sorted(ALLOWED_INTERVALS)}"
        )
    return interval


def normalize_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValueError("El símbolo no puede estar vacío")
    return symbol


def parse_binance_kline(kline: list) -> Candle:
    return Candle(
        open_time=int(kline[0]),
        open=float(kline[1]),
        high=float(kline[2]),
        low=float(kline[3]),
        close=float(kline[4]),
        volume=float(kline[5]),
        close_time=int(kline[6]),
        is_closed=True,
    )


def fetch_historical_candles(
    symbol: str = DEFAULT_SYMBOL,
    interval: str = "1m",
    limit: int = DEFAULT_LIMIT,
) -> HistoricalCandlesResponse:
    symbol = normalize_symbol(symbol)
    interval = validate_interval(interval)

    if limit <= 0:
        raise ValueError("El límite debe ser mayor que 0")

    url = f"{BINANCE_REST_BASE}{KLINES_ENDPOINT}"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    raw_klines = response.json()
    candles = [parse_binance_kline(kline) for kline in raw_klines]

    return HistoricalCandlesResponse(
        symbol=symbol,
        interval=interval,
        source="binance_rest",
        count=len(candles),
        candles=candles,
    )


if __name__ == "__main__":
    data = fetch_historical_candles()
    print(f"symbol={data.symbol} interval={data.interval} count={data.count}")
    if data.candles:
        print("first:", data.candles[0].model_dump())
        print("last:", data.candles[-1].model_dump())
