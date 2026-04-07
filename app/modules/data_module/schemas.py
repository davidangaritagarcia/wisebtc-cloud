from pydantic import BaseModel, Field


class Candle(BaseModel):
    open_time: int = Field(..., description="Timestamp de apertura en milisegundos")
    open: float = Field(..., description="Precio de apertura")
    high: float = Field(..., description="Precio máximo")
    low: float = Field(..., description="Precio mínimo")
    close: float = Field(..., description="Precio de cierre")
    volume: float = Field(..., description="Volumen")
    close_time: int = Field(..., description="Timestamp de cierre en milisegundos")
    is_closed: bool = Field(..., description="Indica si la vela ya cerró")


class HistoricalCandlesResponse(BaseModel):
    symbol: str
    interval: str
    source: str
    count: int
    candles: list[Candle]


class LiveCandleMessage(BaseModel):
    symbol: str
    interval: str
    event_type: str
    event_time: int
    candle: Candle
