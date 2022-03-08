from pydantic import BaseModel


class HealthCheck(BaseModel):
    environment: str
    title: str
    description: str
    version: str
