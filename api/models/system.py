from .base import AppModel
from tortoise import fields

__all__ = [
    'User',
]


class User(AppModel):
    username = fields.CharField(64, unique=True, description='用户名')
    password = fields.CharField(64, description='密码')
    nickname = fields.CharField(64, null=True, default='游客')
    status = fields.BooleanField(default=False, description='是否启用')
    is_super = fields.BooleanField(default=False, description='是否管理员')
    order = fields.IntField(null=True, default=0, description='排序')

    class Meta:
        table = 'sys_user'
        table_description = '用户表'

    @classmethod
    async def find_by_username(cls, username: str):
        return await cls.filter(username=username).first()
