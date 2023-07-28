from fastapi_tortoise_crud.model import BaseModel
from tortoise import fields


class User(BaseModel):
    username = fields.CharField(64, unique=True)
    password = fields.CharField(32)
    nickname = fields.CharField(32, null=True, default='游客')

pass
