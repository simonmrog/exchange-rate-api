from fastapi import APIRouter

from app.routes import health, auth, exchange


router = APIRouter()

router.include_router(health.router, prefix="/status")
router.include_router(auth.router, prefix="/auth")
router.include_router(exchange.router, prefix="/exchange")
