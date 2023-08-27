from tortoise import Tortoise
from settings import settings
from auth.auth import get_password_hash
from models import Site, User
from utils.error import ignore_async_errors


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
        print('Creating super user')
        await User.create_one(
            {"username": "admin", "password": get_password_hash("admina"), "nickname": "超级管理员", "status": 1})
    # 如果没有数据，创建一个默认站点
    if not await Site.all().exists():
        await Site.create_one({
            "title": '哈哈导航',
            "icon": 'ion:logo-edge',
            "desc": '哈哈导航',
            "keywords": '哈哈导航',
            "color": '#104A84',
            "footer": '<a href="https://beian.miit.gov.cn/#/Integrated/index" target="_blank">渝ICP备2021008654号</a>2023 - 2023 哈哈导航. All Rights Reserved.'
        })
    await Tortoise.close_connections()
