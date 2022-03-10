from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.logger import get_logger
from app.config import get_settings
from app.db.config import init_tortoise, connect_to_database
from app.db.defaults import create_default_user
from app.routes.api import router
from app.debugger import init_debugger


log = get_logger(__name__)
settings = get_settings()


def init_application() -> FastAPI:
    if settings.DEBUGGER is True:
        init_debugger()
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )
    app.include_router(router, prefix="/api")
    return app


app = init_application()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_tortoise(app)
    await connect_to_database()
    await create_default_user()


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
