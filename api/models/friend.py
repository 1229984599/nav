from .base import AppModel
from tortoise import fields


class Friend(AppModel):
    title = fields.CharField(100, unique=True)
    href = fields.CharField(200)
    icon = fields.CharField(128, null=True)
    desc = fields.TextField(null=True)
    color = fields.CharField(20, null=True, description='图标颜色hex')
    order = fields.IntField(null=True, default=0, index=True, description='值越大越靠前')
    # menus: fields.ManyToManyRelation[Menu]
