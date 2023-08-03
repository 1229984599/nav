from api.system.utils import get_password_hash
from models import Site, User


async def init_data():
    # 初始化数据
    # 创建一个超级管理员
    await User.create_one({"username": "admin", "password": get_password_hash("admin"), "nickname": "超级管理员"})
    await Site.create_one({
        "title": '哈哈导航',
        "icon": 'cryptocurrency:nav',
        "desc": '哈哈导航',
        "keywords": '哈哈导航',
        "color": '#1E90FF'
    })
