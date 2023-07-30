from core.db import BaseModel
from tortoise import fields


# 站点相关信息
class SiteInfo(BaseModel):
    site_name = fields.CharField(16, default='哈哈导航')
