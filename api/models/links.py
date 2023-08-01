from core.db import BaseModel
from tortoise import fields


class Links(BaseModel):
    title = fields.CharField(100, unique=True)
    href = fields.CharField(200)
    icon = fields.CharField(128, null=True)
    is_self = fields.BooleanField(default=False)
    desc = fields.TextField(null=True)
    color = fields.CharField(7, null=True, description='图标颜色hex')
    order = fields.IntField(null=True, default=0, description='值越大越靠前')
    # menus: fields.ManyToManyRelation[Menu]
