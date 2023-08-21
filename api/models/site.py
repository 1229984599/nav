from fastapi_tortoise_crud import BaseModel
from tortoise import fields


class Site(BaseModel):
    title = fields.CharField(100, description='网站标题')
    desc = fields.TextField(null=True, description='站点描述')
    keywords = fields.CharField(256, null=True, description='站点关键字')
    icon = fields.CharField(128, null=True, description='图标地址')
    color = fields.CharField(7, null=True, description='图标颜色hex')
    footer = fields.TextField(null=True, description='底部版权信息等')
