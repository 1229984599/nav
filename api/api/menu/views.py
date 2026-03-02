from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from auth.auth import get_current_user, is_login
from common.errors import not_found
from common.response import BaseApiOut
from models import Menu, User
from .service import (
    clear_menu_cache,
    create_menus_batch,
    normalize_parent_id,
    parse_menu_order_by,
    update_menus_batch,
)
from .schemas import MenuSchemaFilters, MenuSchemaList, MenuSchemaUpdate, MenuUpdateAllSchema

menu_router = APIRouter()


@menu_router.post("/list", response_model=BaseApiOut[Page[MenuSchemaList]])
async def handle_menu_list(filters: MenuSchemaFilters, params: Params = Depends(), order_by: str = "-create_time"):
    query = Menu.all()
    item = filters.model_dump(exclude_unset=True)
    if item.get("title"):
        query = query.filter(title__icontains=item["title"])
    if item.get("status") is not None:
        query = query.filter(status=item["status"])
    if item.get("parent_id") == 0:
        query = query.filter(parent_id=None)
    elif item.get("parent_id"):
        query = query.filter(parent_id=item["parent_id"])
    query = query.order_by(*parse_menu_order_by(order_by))
    data = await paginate(query, params, True)
    return BaseApiOut(data=data)


@menu_router.get("/read/{item_id}", response_model=BaseApiOut[MenuSchemaList])
async def handle_menu_read(item_id: str):
    item = await Menu.get_or_none(id=item_id)
    if not item:
        return not_found("菜单")
    return BaseApiOut(data=MenuSchemaList.model_validate(item, from_attributes=True))


@menu_router.post("/create", response_model=BaseApiOut[MenuSchemaUpdate], dependencies=[Depends(get_current_user)])
async def handle_menu_create(item: MenuSchemaUpdate):
    await clear_menu_cache()
    payload = item.model_dump(exclude_unset=True)
    payload["parent_id"] = normalize_parent_id(payload.pop("parent_id", None))
    data = await Menu.create(**payload)
    return BaseApiOut(data=MenuSchemaUpdate.model_validate(data, from_attributes=True))


@menu_router.post("/create/all", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_menu_create_all(items: list[MenuSchemaUpdate]):
    await clear_menu_cache()
    await create_menus_batch(items)
    return BaseApiOut(message="批量创建成功")


@menu_router.put("/{item_id}", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_menu_update(item_id: str, item: MenuSchemaUpdate):
    await clear_menu_cache()
    menu = await Menu.get_or_none(id=item_id)
    if not menu:
        return not_found("菜单")
    payload = item.model_dump(exclude_unset=True)
    if "parent_id" in payload:
        payload["parent_id"] = normalize_parent_id(payload["parent_id"])
    data = await Menu.filter(id=item_id).update(**payload)
    return BaseApiOut(data=data)


@menu_router.put("/update/all", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_menu_update_all(items: list[MenuUpdateAllSchema]):
    await clear_menu_cache()
    await update_menus_batch(items)
    return BaseApiOut(message="批量更新成功")


@menu_router.delete("/{item_ids}", response_model=BaseApiOut)
async def handle_menu_delete(item_ids: str):
    ids = item_ids.split(",")
    data = await Menu.filter(id__in=ids).delete()
    return BaseApiOut(data=data)


@menu_router.delete("/delete/all", response_model=BaseApiOut)
async def handle_menu_delete_all():
    await Menu.all().delete()
    return BaseApiOut(message="删除所有数据成功")


async def get_menu_tree(menu_item: Menu, user) -> dict:
    link_query = menu_item.links.order_by("order")
    if not user:
        link_query = link_query.filter(is_vip=False)
    links = await link_query.all().values()
    menu_tree = {
        "id": menu_item.id,
        "title": menu_item.title,
        "icon": menu_item.icon,
        "color": menu_item.color,
        "links": links,
        "is_vip": menu_item.is_vip,
        "status": menu_item.status,
        "order": menu_item.order,
        "create_time": menu_item.create_time,
        "parent_id": menu_item.parent_id,
    }
    children = await menu_item.children.all().order_by("order")
    if children:
        menu_tree["children"] = [await get_menu_tree(child, user) for child in children]
    return menu_tree


@menu_router.get("/tree", description="返回菜单树", response_model=BaseApiOut)
async def handle_get_menu_tree(user: User = Depends(is_login)):
    all_menu_items = await Menu.all().order_by("order").prefetch_related("links", "children__children")
    menu_tree = []
    for menu_item in all_menu_items:
        if not menu_item.parent:
            menu_tree.append(await get_menu_tree(menu_item, user))
    return BaseApiOut(data=menu_tree)
