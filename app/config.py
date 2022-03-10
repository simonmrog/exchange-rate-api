from pydantic import BaseSettings


from app.logger import get_logger


log = get_logger(__name__)


class Settings(BaseSettings):
    DEBUGGER: bool
    ENVIRONMENT: str
    APP_TITLE: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_TEST_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    OFFICIAL_RATE_SITE: str
    FIXER_API: str
    FIXER_API_KEY: str
    BANXICO_API: str
    BANXICO_TOKEN: str
    RATE_LIMIT_PER_USER: int


settings = Settings()
