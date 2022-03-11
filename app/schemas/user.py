from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    password: str
    rate_limit: Optional[int] = Field(0)


class UserAuth(BaseModel):
    id: int
    username: str
    rate_limit: int


class UpdateUser(BaseModel):
    rate_limit: int
