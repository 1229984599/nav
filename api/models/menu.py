from fastapi_tortoise_crud import BaseModel
from tortoise import fields


class Menu(BaseModel):
    title = fields.CharField(64, unique=True)
    icon = fields.CharField(64, default='ic:round-menu', description='图标字符串')
    # parent_id = fields.IntField(default=0, description='父id')
    parent = fields.ForeignKeyField('models.Menu', related_name='children', null=True)
    order = fields.IntField(default=0, description='值越大越靠前')
    color = fields.CharField(7, null=True, description='图标颜色hex')
    links = fields.ManyToManyField("models.Links", related_name="menus", null=True)
    is_vip = fields.BooleanField(default=False, description='是否是vip菜单，登录后才能查看')
