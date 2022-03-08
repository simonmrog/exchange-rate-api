from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from app.schemas.exchange import ExchangeResult
from app.config import settings
from app.core.httpx import HTTPClient


class ExchangeService:
    def __init__(self):
        self.__client = HTTPClient()

    def __extract_official_rate(self, html: str) -> ExchangeResult:
        site = BeautifulSoup(html, "html.parser")
        table_cells = site.select("tr.renglonNon > td")
        if len(table_cells) < 4:
            raise Exception("Could not get rates from {settings.OFFICIAL_RATE_SITE}")
        date = table_cells[0].text
        date = date.replace("\r", "").replace("\n", "").replace(" ", "")
        rate = table_cells[3].text
        rate = rate.replace("\r", "").replace("\n", "").replace(" ", "")
        last_updated = datetime.strptime(date, "%d/%m/%Y").isoformat()
        return ExchangeResult(last_updated=last_updated, value=float(rate))

    async def get_official_data(self) -> ExchangeResult:
        url = f"{settings.OFFICIAL_RATE_SITE}"
        response = await self.__client.get(url=url)
        mxn_rate = self.__extract_official_rate(html=response.text)
        return mxn_rate

    async def get_data_from_fixer(self) -> ExchangeResult:
        url = f"{settings.FIXER_API}?access_key={settings.FIXER_API_KEY}"
        response = await self.__client.get(url=url)
        rates = response.json()
        mxn_rate = rates["rates"]["MXN"]
        timestamp = rates["timestamp"]
        last_updated = datetime.utcfromtimestamp(timestamp).isoformat()
        return ExchangeResult(last_updated=last_updated, value=mxn_rate)

    async def get_data_from_banxico(self) -> ExchangeResult:
        today = datetime.today().strftime("%Y-%m-%d")
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        url = f"{settings.BANXICO_API}/{yesterday}/{today}"
        auth = {"Bmx-Token": settings.BANXICO_TOKEN}
        response = await self.__client.get(url=url, headers=auth)
        rates = response.json()
        series = rates["bmx"]["series"][0]["datos"]
        mxn_rate = series[-1]["dato"]
        last_updated = datetime.strptime(series[-1]["fecha"], "%d/%m/%Y").isoformat()
        return ExchangeResult(last_updated=last_updated, value=mxn_rate)


exchange_service = ExchangeService()
