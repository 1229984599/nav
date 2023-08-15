from tortoise import Tortoise
from settings import settings
from core.auth import get_password_hash
from models import Site, User
from utils.utils import ignore_async_errors


@ignore_async_errors
async def init_data():
    # 初始化数据
    await Tortoise.init(
        config=settings.DATABASE_CONFIG
    )
    # 创建表
    await Tortoise.generate_schemas()
    # 如果没有数据，创建一个超级管理员
    if not await User.all().exists():
        await User.create_one({"username": "admin", "password": get_password_hash("admin"), "nickname": "超级管理员"})
    # 如果没有数据，创建一个默认站点
    if not await Site.all().exists():
        await Site.create_one({
            "title": '哈哈导航',
            "icon": 'ion:logo-edge',
            "desc": '哈哈导航',
            "keywords": '哈哈导航',
            "color": '#104A84'
        })
    await Tortoise.close_connections()
