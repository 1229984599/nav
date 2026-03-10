import asyncio
import json
import time

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import Response
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from auth.auth import get_current_user, get_current_super_user, is_login
from common.errors import not_found
from common.response import BaseApiOut
from models import Links, Menu, User
from .service import (
    clear_menu_cache,
    create_menus_batch,
    normalize_parent_id,
    parse_menu_order_by,
    update_menus_batch,
)
from .schemas import MenuImportRequest, MenuSchemaFilters, MenuSchemaList, MenuSchemaUpdate, MenuUpdateAllSchema

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


@menu_router.post("/import-json", dependencies=[Depends(get_current_user)])
async def handle_menu_import_json(payload: MenuImportRequest):
    """从前端预览后的JSON数据导入菜单"""
    created = 0
    skipped = 0

    # 第一遍：创建所有菜单（不设置parent）
    for item in payload.items:
        if not item.title:
            skipped += 1
            continue
        exists = await Menu.filter(title=item.title).first()
        if exists:
            skipped += 1
            continue
        await Menu.create(
            title=item.title,
            icon=item.icon,
            color=item.color,
            order=item.order,
            is_vip=item.is_vip,
            status=item.status,
        )
        created += 1

    # 第二遍：设置父级关系
    for item in payload.items:
        if not item.parent_title:
            continue
        menu = await Menu.filter(title=item.title).first()
        parent = await Menu.filter(title=item.parent_title).first()
        if menu and parent:
            menu.parent_id = parent.id
            await menu.save()

    await clear_menu_cache()
    return BaseApiOut(data={"created": created, "skipped": skipped})


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


@menu_router.get("/impact", dependencies=[Depends(get_current_user)])
async def handle_menu_impact(ids: str = Query(...)):
    """查询删除菜单的影响：子菜单数量、关联链接数量"""
    id_list = [int(x) for x in ids.split(",") if x.strip()]
    id_set = set(id_list)

    # Find children not already in the selection
    children = await Menu.filter(parent_id__in=id_list).all()
    external_children = [c for c in children if c.id not in id_set]
    child_count = len(external_children)

    # Count links associated with these menus (M2M)
    menus = await Menu.filter(id__in=id_list).prefetch_related("links")
    link_ids = set()
    menu_titles = []
    for m in menus:
        menu_titles.append(m.title)
        for link in m.links:
            link_ids.add(link.id)
    link_count = len(link_ids)

    return BaseApiOut(data={
        "child_count": child_count,
        "link_count": link_count,
        "menu_titles": menu_titles,
    })


@menu_router.delete("/{item_ids}", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_menu_delete(
    item_ids: str,
    children_action: str = Query("move_up", regex="^(move_up|delete)$"),
    links_action: str = Query("unlink", regex="^(unlink|delete)$"),
):
    ids = [int(x) for x in item_ids.split(",") if x.strip()]
    id_set = set(ids)

    async def _delete_menus(menu_ids: list[int]):
        """Delete menus and handle children/links based on action params."""
        menus = await Menu.filter(id__in=menu_ids).prefetch_related("links")
        for menu in menus:
            # Handle links
            if links_action == "delete":
                link_list = list(menu.links)
                if link_list:
                    await Links.filter(id__in=[l.id for l in link_list]).delete()
            else:
                await menu.links.clear()

            # Handle children
            children = await Menu.filter(parent_id=menu.id).all()
            if children:
                if children_action == "delete":
                    child_ids = [c.id for c in children if c.id not in id_set]
                    if child_ids:
                        await _delete_menus(child_ids)
                else:
                    # move_up: reparent children to this menu's parent
                    await Menu.filter(parent_id=menu.id).update(parent_id=menu.parent_id)

        await Menu.filter(id__in=menu_ids).delete()

    await _delete_menus(ids)
    await clear_menu_cache()
    return BaseApiOut()


@menu_router.delete("/delete/all", response_model=BaseApiOut, dependencies=[Depends(get_current_super_user)])
async def handle_menu_delete_all():
    await Menu.all().delete()
    await clear_menu_cache()
    return BaseApiOut(message="删除所有数据成功")


def serialize_link(link: Links) -> dict:
    return {
        "id": link.id,
        "title": link.title,
        "href": link.href,
        "icon": link.icon,
        "is_self": link.is_self,
        "is_vip": link.is_vip,
        "desc": link.desc,
        "color": link.color,
        "order": link.order,
        "cdn_img_id": link.cdn_img_id,
        "status": link.status,
        "create_time": link.create_time.isoformat() if link.create_time else None,
        "update_time": link.update_time.isoformat() if link.update_time else None,
    }


def serialize_menu(menu_item: Menu, user: User | None) -> dict:
    links = sorted(menu_item.links, key=lambda item: item.order or 0)
    if not user:
        links = [item for item in links if not item.is_vip]
    return {
        "id": menu_item.id,
        "title": menu_item.title,
        "icon": menu_item.icon,
        "color": menu_item.color,
        "links": [serialize_link(link) for link in links],
        "is_vip": menu_item.is_vip,
        "status": menu_item.status,
        "order": menu_item.order,
        "create_time": menu_item.create_time.isoformat() if menu_item.create_time else None,
        "parent_id": menu_item.parent_id,
    }


# ---- In-memory cache for /tree ----
_tree_cache: dict[str, dict] = {}
# key: "guest" | "user", value: {"bytes": pre-serialized JSON bytes, "ts": timestamp}
_TREE_CACHE_TTL = 3600 * 24  # 24 hours


def invalidate_tree_cache():
    _tree_cache.clear()
    # Schedule background re-warm so next request hits warm cache
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(_safe_warm())
    except RuntimeError:
        pass


async def _safe_warm():
    """Re-warm cache in background after invalidation."""
    try:
        await warm_tree_cache()
    except Exception:
        pass


async def warm_tree_cache():
    """Pre-build and cache tree data for both guest and user at startup."""
    for cache_key, user in [("guest", None), ("user", True)]:
        root_nodes = await _build_tree(user)
        result = {"code": 200, "message": "请求成功", "msg": "请求成功", "data": root_nodes}
        json_bytes = json.dumps(result, ensure_ascii=False).encode("utf-8")
        _tree_cache[cache_key] = {"bytes": json_bytes, "ts": time.time()}


async def _build_tree(user: User | None) -> list[dict]:
    all_menu_items = await Menu.all().order_by("order").prefetch_related("links")
    menu_map: dict[int, dict] = {}
    root_nodes: list[dict] = []

    for menu_item in all_menu_items:
        menu_map[menu_item.id] = serialize_menu(menu_item, user)

    for menu_item in all_menu_items:
        current_node = menu_map[menu_item.id]
        parent_id = menu_item.parent_id
        if parent_id and parent_id in menu_map:
            parent_node = menu_map[parent_id]
            parent_node.setdefault("children", []).append(current_node)
            continue
        root_nodes.append(current_node)

    return root_nodes


@menu_router.get("/tree", description="返回菜单树")
async def handle_get_menu_tree(user: User = Depends(is_login)):
    cache_key = "user" if user else "guest"
    now = time.time()
    cached = _tree_cache.get(cache_key)
    if cached and (now - cached["ts"]) < _TREE_CACHE_TTL:
        return Response(content=cached["bytes"], media_type="application/json")

    root_nodes = await _build_tree(user)
    result = {"code": 200, "message": "请求成功", "msg": "请求成功", "data": root_nodes}
    json_bytes = json.dumps(result, ensure_ascii=False).encode("utf-8")
    _tree_cache[cache_key] = {"bytes": json_bytes, "ts": now}
    return Response(content=json_bytes, media_type="application/json")


def _serialize_menu(menu, parent_title=None):
    return {
        "title": menu.title,
        "icon": menu.icon,
        "color": menu.color,
        "order": menu.order,
        "is_vip": menu.is_vip,
        "status": menu.status,
        "parent_title": parent_title,
    }


@menu_router.get("/export", dependencies=[Depends(get_current_user)])
async def handle_menu_export():
    """导出所有菜单数据为JSON"""
    menus = await Menu.all().order_by("order").select_related("parent")
    data = []
    for menu in menus:
        parent_title = menu.parent.title if menu.parent else None
        data.append(_serialize_menu(menu, parent_title))
    content = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=menus.json"},
    )


@menu_router.post("/import", dependencies=[Depends(get_current_user)])
async def handle_menu_import(file: UploadFile = File(...)):
    """从JSON文件导入菜单数据"""
    content = await file.read()
    try:
        items = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON格式错误")
    if not isinstance(items, list):
        raise HTTPException(status_code=400, detail="数据格式错误，应为数组")

    created = 0
    skipped = 0

    # 第一遍：创建所有菜单（不设置parent）
    for item in items:
        title = item.get("title")
        if not title:
            skipped += 1
            continue
        exists = await Menu.filter(title=title).first()
        if exists:
            skipped += 1
            continue
        await Menu.create(
            title=title,
            icon=item.get("icon", "ic:round-menu"),
            color=item.get("color"),
            order=item.get("order", 0),
            is_vip=item.get("is_vip", False),
            status=item.get("status", True),
        )
        created += 1

    # 第二遍：设置父级关系
    for item in items:
        parent_title = item.get("parent_title")
        if not parent_title:
            continue
        menu = await Menu.filter(title=item.get("title")).first()
        parent = await Menu.filter(title=parent_title).first()
        if menu and parent:
            menu.parent_id = parent.id
            await menu.save()

    await clear_menu_cache()
    return BaseApiOut(data={"created": created, "skipped": skipped})
