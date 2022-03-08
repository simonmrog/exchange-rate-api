from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUGGER: bool
    ENVIRONMENT: str
    APP_TITLE: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    FIXER_API: str
    FIXER_API_KEY: str
    BANXICO_API: str
    BANXICO_TOKEN: str


settings = Settings()
