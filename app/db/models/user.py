from tortoise.models import Model
from tortoise import fields


class User(Model):
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    rate_limit = fields.IntField(default=0)
