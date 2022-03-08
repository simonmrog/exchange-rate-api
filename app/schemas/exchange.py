from typing import Dict
from pydantic import BaseModel


class ExchangeResult(BaseModel):
    last_updated: str
    value: float


class ExchangeOutput(BaseModel):
    rates: Dict[str, ExchangeResult]
