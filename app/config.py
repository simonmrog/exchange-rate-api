from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUGGER: bool
    ENVIRONMENT: str
    APP_TITLE: str
    APP_DESCRIPTION: str
    APP_VERSION: str


settings = Settings()
