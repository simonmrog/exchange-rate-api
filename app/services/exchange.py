from datetime import datetime

from app.schemas.exchange import ExchangeResult
from app.config import settings
from app.core.httpx import HTTPClient


class ExchangeService:
    def __init__(self):
        self.__client = HTTPClient()

    async def get_official_data(self) -> ExchangeResult:
        return ExchangeResult(last_updated="official", value=22)

    async def get_data_from_fixer(self) -> ExchangeResult:
        url = f"http://data.fixer.io/api/latest?access_key={settings.FIXER_API_KEY}"
        response = await self.__client.get(url=url)
        mxn_rate = response["rates"]["MXN"]
        timestamp = response["timestamp"]
        last_updated = datetime.utcfromtimestamp(timestamp).isoformat()
        return ExchangeResult(last_updated=last_updated, value=mxn_rate)

    async def get_data_from_banxico(self) -> ExchangeResult:
        return ExchangeResult(last_updated="banxico", value=22)


exchange_service = ExchangeService()
