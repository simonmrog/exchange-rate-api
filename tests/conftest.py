import asyncio

import pytest

from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.config import settings
from app.main import init_application


@pytest.fixture(scope="function", autouse=True)
def test_app():
    app = init_application()
    db_auth = f"{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}"
    db_url = (
        f"postgres://{db_auth}@{settings.DATABASE_HOST}/{settings.DATABASE_TEST_NAME}"
    )
    initializer(
        ["app.db.models"],
        db_url=db_url,
    )
    with TestClient(app) as test_client:
        yield test_client
    finalizer()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
