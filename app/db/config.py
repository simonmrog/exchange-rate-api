from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


from app.logger import get_logger
from app.config import settings


log = get_logger(__name__)
database_auth = f"{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}"
database_url = (
    f"postgres://{database_auth}@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}"
)


def init_tortoise(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=database_url,
        modules={"models": ["app.db.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


async def connect_to_database() -> None:
    log.info("Initializing Tortoise...")
    await Tortoise.init(db_url=database_url, modules={"models": ["app.db.models"]})
    log.info("Generating database schemas via Tortoise...")
    await Tortoise.generate_schemas()
