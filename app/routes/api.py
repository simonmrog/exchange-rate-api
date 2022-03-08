from fastapi import APIRouter

from app.routes import health, exchange


router = APIRouter()

router.include_router(health.router, prefix="/status")
router.include_router(exchange.router, prefix="/exchange")
