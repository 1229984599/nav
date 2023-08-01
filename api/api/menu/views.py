from core.crud import ModelCrud, BaseApiOut
from models import Menu, Links
from .schemas import SetLinkSchema

menu_router = ModelCrud(Menu, schema_filters=Menu.schema_filters(include=('title',))).register_crud()


# 递归函数，用于获取菜单树
async def get_menu_tree(menu_item: Menu) -> dict:
    menu_tree = {
        "id": menu_item.id,
        "title": menu_item.title,
        "icon": menu_item.icon,
        "color": menu_item.color,
        "links": await menu_item.links
    }
    children = await menu_item.children
    if children:
        menu_tree["children"] = [await get_menu_tree(child) for child in children]
    return menu_tree


@menu_router.get('/tree', description='返回菜单树')
async def handle_get_menu_tree():
    all_menu_items = await Menu.all().prefetch_related(
        "links", "children__children")
    menu_tree = []
    for menu_item in all_menu_items:
        if not menu_item.parent:  # 只处理根级菜单
            menu_tree.append(await get_menu_tree(menu_item))
    return BaseApiOut(data=menu_tree)


@menu_router.post('/set_link', description='设置导航菜单')
async def handle_set_menu(set_link: SetLinkSchema):
    """
    设置导航菜单
    """
    menu = await Menu.find_one(id=set_link.menu_id)
    if not menu:
        return BaseApiOut(code=400, message='菜单不存在')
    links = await Links.filter(id__in=set_link.links).all()
    if not links:
        return BaseApiOut(code=400, message='导航不存在')
    await menu.links.clear()
    await menu.links.add(*links)
    return BaseApiOut(message='设置导航成功')
