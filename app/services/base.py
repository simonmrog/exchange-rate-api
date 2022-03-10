from typing import Dict, Any
from tortoise.models import Model
from pydantic import BaseModel


class BaseService:
    def __init__(self, model: Model):
        self.model = model

    async def find(self, *, payload: Dict[str, Any]):
        model_objs = await self.model.filter(**payload)
        return model_objs

    async def create(self, *, payload: BaseModel) -> BaseModel:
        payload_data = payload.dict()
        model_obj = await self.model.create(**payload_data)
        return model_obj
