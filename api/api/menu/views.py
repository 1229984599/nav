from fastapi import Depends

from tortoise.queryset import QuerySet

from core.crud import ModelCrud, BaseApiOut
from models import Menu, Links, User
from .schemas import SetLinkSchema, MenuSchemaList, MenuSchemaUpdate
from core.auth import get_current_user,is_login


class MenuCrud(ModelCrud):
    @classmethod
    async def pre_list(cls, queryset: QuerySet, item: dict) -> QuerySet:
        return await super().pre_list(queryset, item)

    @classmethod
    async def pre_update(cls, item: MenuSchemaUpdate, item_id=None) -> dict:
        if not item.parent_id:
            item.parent_id = None
        return item.dict(exclude_unset=True)


menu_router = MenuCrud(Menu, schema_list=MenuSchemaList,
                       schema_update=MenuSchemaUpdate,
                       schema_filters=Menu.schema_filters(include=('title',))
                       ).register_crud(
    depends_create=[Depends(get_current_user)],
    depends_update=[Depends(get_current_user)],
)


# 递归函数，用于获取菜单树
async def get_menu_tree(menu_item: Menu, user) -> dict:
    link_query = menu_item.links
    if not user:
        link_query = link_query.filter(is_vip=False)
    menu_tree = {
        "id": menu_item.id,
        "title": menu_item.title,
        "icon": menu_item.icon,
        "color": menu_item.color,
        "links": await link_query,
        "order": menu_item.order,
        "create_time": menu_item.create_time,
        "parent_id": menu_item.parent_id,
    }
    children = await menu_item.children
    if children:
        menu_tree["children"] = [await get_menu_tree(child) for child in children]
    return menu_tree


@menu_router.get('/tree', description='返回菜单树')
async def handle_get_menu_tree(user: User = Depends(is_login)):
    queryset = Menu.all()
    all_menu_items = await queryset.order_by('order').prefetch_related(
        "links", "children__children")
    menu_tree = []
    for menu_item in all_menu_items:
        if not menu_item.parent:  # 只处理根级菜单
            menu_tree.append(await get_menu_tree(menu_item, user))
    return BaseApiOut(data=menu_tree)

# @menu_router.post('/set_link', description='设置导航菜单')
# async def handle_set_menu(set_link: SetLinkSchema):
#     """
#     设置导航菜单
#     """
#     menu = await Menu.find_one(id=set_link.menu_id)
#     if not menu:
#         return BaseApiOut(code=400, message='菜单不存在')
#     links = await Links.filter(id__in=set_link.links).all()
#     if not links:
#         return BaseApiOut(code=400, message='导航不存在')
#     await menu.links.clear()
#     await menu.links.add(*links)
#     return BaseApiOut(message='设置导航成功')
