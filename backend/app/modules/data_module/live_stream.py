import asyncio
import json
from urllib.parse import urljoin

import websockets

from .config import BINANCE_WS_BASE, DEFAULT_INTERVAL, DEFAULT_SYMBOL
from .schemas import Candle, LiveCandleMessage
from .storage import save_live_message


def build_stream_name(symbol: str, interval: str) -> str:
    return f"{symbol.lower()}@kline_{interval}"


def build_ws_url(symbol: str, interval: str) -> str:
    stream_name = build_stream_name(symbol, interval)
    return urljoin(f"{BINANCE_WS_BASE}/", stream_name)


def parse_kline_message(raw_message: str) -> LiveCandleMessage:
    payload = json.loads(raw_message)

    event_type = payload["e"]
    event_time = int(payload["E"])
    symbol = payload["s"]
    k = payload["k"]

    candle = Candle(
        open_time=int(k["t"]),
        open=float(k["o"]),
        high=float(k["h"]),
        low=float(k["l"]),
        close=float(k["c"]),
        volume=float(k["v"]),
        close_time=int(k["T"]),
        is_closed=bool(k["x"]),
    )

    return LiveCandleMessage(
        symbol=symbol,
        interval=k["i"],
        event_type=event_type,
        event_time=event_time,
        candle=candle,
    )


async def stream_live_candles(
    symbol: str = DEFAULT_SYMBOL,
    interval: str = DEFAULT_INTERVAL,
    max_messages: int = 5,
) -> None:
    url = build_ws_url(symbol, interval)
    print(f"CONNECTING_WS: {url}")

    received = 0

    async with websockets.connect(url) as websocket:
        async for raw_message in websocket:
            message = parse_kline_message(raw_message)
            path = save_live_message(message)

            print("LIVE_OK")
            print(
                f"symbol={message.symbol} interval={message.interval} "
                f"close={message.candle.close} closed={message.candle.is_closed}"
            )
            print(f"saved_to={path}")

            received += 1
            if received >= max_messages:
                print("STREAM_DONE")
                break


if __name__ == "__main__":
    asyncio.run(stream_live_candles())
