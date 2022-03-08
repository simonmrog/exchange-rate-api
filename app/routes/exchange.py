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
        official_result = await exchange_service.get_official_data()
        fixer_result = await exchange_service.get_data_from_fixer()
        banxico_result = await exchange_service.get_data_from_banxico()

        return ExchangeOutput(
            rates={
                "official": official_result,
                "fixer": fixer_result,
                "banxico": banxico_result,
            }
        )
    except Exception as e:
        error_handler.handle_error(e)
