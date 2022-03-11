from asyncio import gather
from fastapi import APIRouter, status, Security, HTTPException

from app.logger import get_logger
from app.config import settings
from app.schemas.user import UserAuth, UpdateUser
from app.schemas.exchange import ExchangeOutput
from app.services.exchange import exchange_service
from app.services.auth import auth_service
from app.services.user import user_service
from app.services.error import error_handler


log = get_logger(__name__)
router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ExchangeOutput,
)
async def get_exchange(
    current_user: UserAuth = Security(auth_service.get_current_user),
):
    try:
        user = await user_service.find_by_id(id=current_user.id)
        if user is None:
            raise HTTPException(
                status_code=403,
                detail="Could not validate credentials. Please login again",
            )
        user_rate_limit = user["rate_limit"]
        if user_rate_limit > settings.RATE_LIMIT_PER_USER:
            raise HTTPException(
                status_code=403,
                detail="Rate limit exceeded. Please upgrade your subscription",
            )
        official_result = exchange_service.get_official_data()
        # fixer_result = exchange_service.get_data_from_fixer()
        banxico_result = exchange_service.get_data_from_banxico()
        rates = await gather(official_result, banxico_result)
        rate_results = [rates[0], {"last_updated": "today", "value": 20}, rates[1]]
        # rate_results = await gather(official_result, fixer_result, banxico_result)

        patch = UpdateUser(rate_limit=user_rate_limit + 1)
        await user_service.update(id=current_user.id, payload=patch)
        return ExchangeOutput(
            rates={
                "official": rate_results[0],
                "fixer": rate_results[1],
                "banxico": rate_results[2],
            }
        )
    except Exception as e:
        error_handler.handle_error(e)
