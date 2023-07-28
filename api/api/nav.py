from fastapi_tortoise_crud import ModelCrud, BaseApiOut
from pydantic import BaseModel

from models import NavItem, Menu
from utils.site import get_site_info

nav_router = ModelCrud(NavItem).register_crud()


class SetMenuSchema(BaseModel):
    menus: list[int]
    nav_id: int


@nav_router.post('/set_menu')
async def handle_set_menu(set_menu: SetMenuSchema):
    """
    设置导航菜单
    """
    nav = await NavItem.find_one(id=set_menu.nav_id)
    if not nav:
        return BaseApiOut(code=400, message='导航不存在')
    menus = await Menu.filter(id__in=set_menu.menus).all()
    if not menus:
        return BaseApiOut(code=400, message='菜单不存在')
    await nav.menus.clear()
    await nav.menus.add(*menus)
    return BaseApiOut(message='设置导航菜单成功')


@nav_router.post('/siteinfo')
async def handle_sietinfo(url: str):
    data = await get_site_info(url)
    return BaseApiOut(data=data)
