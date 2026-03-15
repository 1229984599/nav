from .base import AppModel
from tortoise import fields


class CorsOrigin(AppModel):
    origin = fields.CharField(255, unique=True, description='允许的域名')
    desc = fields.CharField(255, default='', description='备注')
    order = fields.IntField(null=True, default=0, index=True, description='排序')

    class Meta:
        table = "cors_origin"
        ordering = ["order"]
