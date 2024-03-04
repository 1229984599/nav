from fastapi_tortoise_crud import BaseModel
from tortoise import fields


class Links(BaseModel):
    title = fields.CharField(100, unique=True)
    href = fields.CharField(200)
    icon = fields.CharField(128, null=True)
    is_self = fields.BooleanField(default=False, description='是否站内打开')
    is_vip = fields.BooleanField(default=False, description='是否vip打开(登录即可）')
    desc = fields.TextField(null=True)
    color = fields.CharField(7, null=True, description='图标颜色hex')
    order = fields.IntField(null=True, default=0, description='值越大越靠前')
    cdn_img_id = fields.IntField(null=True, description='图床的cdn id')
    # menus: fields.ManyToManyRelation[Menu]
