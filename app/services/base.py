from typing import Dict, Any, Optional
from tortoise.models import Model
from pydantic import BaseModel


class BaseService:
    def __init__(self, model: Model):
        self.model = model

    async def find(self, *, payload: Dict[str, Any]):
        model_objs = await self.model.filter(**payload)
        return model_objs

    async def find_by_id(self, *, id: int) -> Optional[Dict[str, Any]]:
        model_obj = await self.model.filter(id=id).first().values()
        return model_obj

    async def create(self, *, payload: BaseModel) -> BaseModel:
        payload_data = payload.dict()
        model_obj = await self.model.create(**payload_data)
        return model_obj

    async def update(self, *, id: int, payload: BaseModel) -> BaseModel:
        payload_data = payload.dict(exclude_unset=True)
        await self.model.filter(id=id).update(**payload_data)
        updated_model_obj = await self.find(payload={"id": id})
        return updated_model_obj
