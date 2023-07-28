from fastapi import Body, Query

from fastapi_tortoise_crud import ModelCrud, BaseApiOut
from models import Menu, NavItem
from utils.faker import faker
from pydantic import BaseModel


class SchemaMenuList(Menu.schema_list(exclude=('parent_id',))):
    pass


menu_router = ModelCrud(Menu, schema_list=SchemaMenuList).register_crud()


@menu_router.post('/faker')
async def handle_faker_data(number: int = Query(default=10)):
    """
    Generate a number of fake users.
    """
    data = await Menu.bulk_create([
        Menu(
            title=faker.name(),
            icon=faker.job()

        ) for i in range(number)], ignore_conflicts=True)
    return BaseApiOut(data=data)
    pass


# 递归函数，用于获取菜单树
async def get_menu_tree(menu_item: Menu) -> dict:
    menu_tree = {
        "id": menu_item.id,
        "title": menu_item.title,
        "icon": menu_item.icon,
        "navs": await menu_item.navs
    }
    children = await menu_item.children
    if children:
        menu_tree["children"] = [await get_menu_tree(child) for child in children]
    return menu_tree


@menu_router.get('/tree', description='返回菜单树')
async def handle_get_menu_tree():
    all_menu_items = await Menu.all().prefetch_related(
        "navs", "children__children")
    menu_tree = []
    for menu_item in all_menu_items:
        if not menu_item.parent:  # 只处理根级菜单
            menu_tree.append(await get_menu_tree(menu_item))
    return BaseApiOut(data=menu_tree)


class SetNavSchema(BaseModel):
    navs: list[int]
    menu_id: int


@menu_router.post('/set_nav', description='设置导航菜单')
async def handle_set_menu(set_nav: SetNavSchema):
    """
    设置导航菜单
    """
    menu = await Menu.find_one(id=set_nav.menu_id)
    if not menu:
        return BaseApiOut(code=400, message='菜单不存在')
    navs = await NavItem.filter(id__in=set_nav.navs).all()
    if not navs:
        return BaseApiOut(code=400, message='导航不存在')
    await menu.navs.clear()
    await menu.navs.add(*navs)
    return BaseApiOut(message='设置导航成功')
