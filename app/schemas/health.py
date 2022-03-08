from pydantic import BaseModel


class HealthCheck(BaseModel):
    title: str
    description: str
    version: str
