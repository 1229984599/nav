from fastapi import Depends
from tortoise.contrib.pydantic import PydanticModel

from fastapi_tortoise_crud import ModelCrud, BaseApiOut
from models import Menu, User, Links
from .schemas import MenuSchemaList, MenuSchemaUpdate, MenuSchemaFilters
from auth.auth import get_current_user, is_login


# from fastapi_cache.decorator import cache


class MenuCrud(ModelCrud):
    @classmethod
    async def pre_list(cls, item: PydanticModel) -> dict:
        search_item = await super().pre_list(item)
        if item.parent_id == 0:
            search_item['parent_id'] = None
        return search_item

    # @classmethod
    # def pre_create(cls, item: PydanticModel) -> dict:
    #     pass

    @classmethod
    async def pre_update(cls, item: PydanticModel, item_id=None) -> dict:
        if not item.parent_id:
            item.parent_id = None
        return item.model_dump(exclude_unset=True)


menu_router = MenuCrud(Menu, schema_list=MenuSchemaList,
                       schema_update=MenuSchemaUpdate,
                       schema_create=MenuSchemaUpdate,
                       schema_filters=MenuSchemaFilters
                       ).register_crud(
    depends_create=[Depends(get_current_user)],
    depends_update=[Depends(get_current_user)],
)


# 递归函数，用于获取菜单树
async def get_menu_tree(menu_item: Menu, user) -> dict:
    link_query = menu_item.links
    if not user:
        link_query = link_query.filter(is_vip=False)
    links = await link_query.all().values()
    menu_tree = {
        "id": menu_item.id,
        "title": menu_item.title,
        "icon": menu_item.icon,
        "color": menu_item.color,
        "links": links,
        "is_vip":menu_item.is_vip,
        "status": menu_item.status,
        "order": menu_item.order,
        "create_time": menu_item.create_time,
        "parent_id": menu_item.parent_id,
    }
    children = await menu_item.children
    if children:
        menu_tree["children"] = [await get_menu_tree(child, user) for child in children]
    return menu_tree


@menu_router.get('/tree', description='返回菜单树', response_model=BaseApiOut)
# @cache(expire=60*30)
async def handle_get_menu_tree(user: User = Depends(is_login)):
    queryset = Menu.all()
    all_menu_items = await queryset.order_by('order').prefetch_related(
        "links", "children__children")
    menu_tree = []
    for menu_item in all_menu_items:
        if not menu_item.parent:  # 只处理根级菜单
            menu_tree.append(await get_menu_tree(menu_item, user))
    return BaseApiOut(data=menu_tree)
