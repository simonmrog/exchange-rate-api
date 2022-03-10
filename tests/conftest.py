import asyncio

import pytest

# from fastapi.testclient import TestClient
# from tortoise.contrib.test import finalizer, initializer

# from app.config import Settings, get_settings
# from app.main import init_application


# def get_settings_override():
#     return Settings(
#         DEBUGGER=False,
#         DATABASE_NAME=os.environ.get("DATABASE_TEST_NAME"),
#     )


# @pytest.fixture(scope="function", autouse=True)
# def test_app():
#     app = init_application()
#     app.dependency_overrides[get_settings] = get_settings_override
#     settings = get_settings()
#     database_auth = f"{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}"
#     database_url = (
#         f"postgres://{database_auth}@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}"
#     )
#     print(database_url)
#     initializer(
#         ["app.db.models"],
#         db_url=database_url,
#     )
#     with TestClient(app) as test_client:
#         yield test_client
#     finalizer()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
