import json
from pathlib import Path
from typing import Any

from .config import get_historical_file, get_live_file
from .schemas import HistoricalCandlesResponse, LiveCandleMessage


def write_json_file(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def save_historical_response(data: HistoricalCandlesResponse) -> Path:
    path = get_historical_file(data.symbol, data.interval)
    payload = data.model_dump()
    write_json_file(path, payload)
    return path


def save_live_message(data: LiveCandleMessage) -> Path:
    path = get_live_file(data.symbol, data.interval)
    payload = data.model_dump()
    write_json_file(path, payload)
    return path
