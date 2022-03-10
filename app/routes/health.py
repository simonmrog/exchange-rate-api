from fastapi import APIRouter

from app.config import get_settings
from app.schemas.health import HealthCheck

settings = get_settings()
router = APIRouter()


@router.get("/")
def health_check() -> HealthCheck:
    return HealthCheck(
        environment=settings.ENVIRONMENT,
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )
