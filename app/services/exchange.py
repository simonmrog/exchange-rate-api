from datetime import datetime, timedelta

from app.schemas.exchange import ExchangeResult
from app.config import settings
from app.core.httpx import HTTPClient


class ExchangeService:
    def __init__(self):
        self.__client = HTTPClient()

    async def get_official_data(self) -> ExchangeResult:
        return ExchangeResult(last_updated="official", value=22)

    async def get_data_from_fixer(self) -> ExchangeResult:
        url = f"{settings.FIXER_API}?access_key={settings.FIXER_API_KEY}"
        response = await self.__client.get(url=url)
        mxn_rate = response["rates"]["MXN"]
        timestamp = response["timestamp"]
        last_updated = datetime.utcfromtimestamp(timestamp).isoformat()
        return ExchangeResult(last_updated=last_updated, value=mxn_rate)

    async def get_data_from_banxico(self) -> ExchangeResult:
        today = datetime.today().strftime("%Y-%m-%d")
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        url = f"{settings.BANXICO_API}/{yesterday}/{today}"
        auth = {"Bmx-Token": settings.BANXICO_TOKEN}
        response = await self.__client.get(url=url, headers=auth)
        series = response["bmx"]["series"][0]["datos"]
        mxn_rate = series[-1]["dato"]
        last_updated = datetime.strptime(series[-1]["fecha"], "%d/%m/%Y").isoformat()
        return ExchangeResult(last_updated=last_updated, value=mxn_rate)


exchange_service = ExchangeService()
