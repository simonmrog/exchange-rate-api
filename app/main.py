from fastapi import FastAPI


from app.config import settings
from app.routes.api import router
from app.debugger import init_debugger


def init_application() -> FastAPI:
    if settings.DEBUGGER is True:
        init_debugger()
    app = FastAPI(
        title=settings.TITLE, description=settings.DESCRIPTION, version=settings.VERSION
    )
    app.include_router(router, prefix="/api")
