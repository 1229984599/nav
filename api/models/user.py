from core.db import BaseModel
from tortoise import fields


class User(BaseModel):
    username = fields.CharField(64, unique=True)
    password = fields.CharField(64)
    nickname = fields.CharField(64, null=True, default='游客')

    @classmethod
    async def find_by_username(cls, username: str):
        return await cls.find_one(username=username)

