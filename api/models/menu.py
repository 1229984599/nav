from fastapi_tortoise_crud import BaseModel
from tortoise import fields


class Menu(BaseModel):

    title = fields.CharField(64, unique=True)
    icon = fields.CharField(64, default='ic:round-menu', description='图标字符串')
    # parent_id = fields.IntField(default=0, description='父id')
    parent = fields.ForeignKeyField('models.Menu', related_name='children', null=True)
    order = fields.IntField(default=0, description='值越大越靠前')
    navs = fields.ManyToManyField("models.NavItem", related_name="menus", blank=True)


class NavItem(BaseModel):
    title = fields.CharField(100, unique=True)
    url = fields.CharField(200)
    icon = fields.CharField(64, null=True)
    is_self = fields.BooleanField(default=False)
    desc = fields.TextField(null=True)
    order = fields.IntField(null=True, default=0, description='值越大越靠前')
