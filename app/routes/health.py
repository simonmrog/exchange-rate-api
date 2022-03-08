from fastapi import APIRouter

from app.config import settings
from app.schemas.health import HealthCheck

router = APIRouter()


@router.get("/")
def health_check() -> HealthCheck:
    return HealthCheck(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )
