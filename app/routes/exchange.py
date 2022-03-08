from asyncio import gather
from fastapi import APIRouter, status

from app.logger import get_logger
from app.schemas.exchange import ExchangeOutput
from app.services.exchange import exchange_service
from app.services.error import error_handler


log = get_logger(__name__)
router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ExchangeOutput,
)
async def get_exchange():
    try:
        official_result = exchange_service.get_official_data()
        fixer_result = exchange_service.get_data_from_fixer()
        banxico_result = exchange_service.get_data_from_banxico()

        rate_results = await gather(official_result, fixer_result, banxico_result)

        return ExchangeOutput(
            rates={
                "official": rate_results[0],
                "fixer": rate_results[1],
                "banxico": rate_results[2],
            }
        )
    except Exception as e:
        error_handler.handle_error(e)
