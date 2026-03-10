import asyncio
import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from auth.auth import get_current_user, get_current_super_user, is_login
from common.errors import not_found
from common.response import BaseApiOut
from models import Links, Menu, User
from .schemas import CreateMenuSchema, FilterSchemaList, LinkImportRequest, LinkSchemaList, LinkUpdateAllSchema
from .service import (
    attach_link_menus,
    build_link_search_filters,
    clear_link_cache,
    create_links_batch,
    parse_order_by,
    sync_link_cdn,
    sync_links_cdn_batch,
    update_links_batch,
)
from .utils import get_site_info

link_router = APIRouter()


@link_router.post("/list", response_model=BaseApiOut[Page[LinkSchemaList]])
async def handle_link_list(
    filters: FilterSchemaList,
    params: Params = Depends(),
    order_by: str = "-create_time",
    user: User = Depends(is_login),
):
    queryset = Links.filter()
    item = filters.model_dump(exclude_unset=True)
    menus = item.pop("menus", None)
    if menus:
        queryset = queryset.filter(menus__in=menus)
    if not user:
        queryset = queryset.filter(is_vip=False)
    queryset = queryset.order_by(*parse_order_by(order_by))
    search_item = build_link_search_filters(item)
    queryset = queryset.filter(**search_item).prefetch_related("menus")
    data = await paginate(queryset, params, True)
    return BaseApiOut(data=data)


@link_router.get("/read/{item_id}", response_model=BaseApiOut[LinkSchemaList])
async def handle_link_read(item_id: str):
    item = await Links.filter(id=item_id).prefetch_related("menus").first()
    if not item:
        return not_found("链接")
    data = LinkSchemaList.model_validate(item, from_attributes=True)
    return BaseApiOut(data=data)


@link_router.post("/create", response_model=BaseApiOut[CreateMenuSchema], dependencies=[Depends(get_current_user)])
async def handle_link_create(item: CreateMenuSchema):
    await clear_link_cache()
    payload = item.model_dump(exclude_unset=True, exclude={"menus"})
    link = await Links.create(**payload)
    await attach_link_menus(link, item.menus)
    return BaseApiOut(data=item)


@link_router.get("/titles", dependencies=[Depends(get_current_user)])
async def handle_link_titles():
    """返回所有链接标题列表（用于导入时重复检测）"""
    titles = await Links.all().values_list("title", flat=True)
    return BaseApiOut(data=titles)


@link_router.post("/create/all", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_link_create_all(items: list[CreateMenuSchema]):
    await clear_link_cache()
    await create_links_batch(items)
    return BaseApiOut(message="批量创建成功")


@link_router.post("/import-json", dependencies=[Depends(get_current_user)])
async def handle_link_import_json(payload: LinkImportRequest):
    """从前端预览后的JSON数据导入链接（后台任务 + WebSocket进度推送）"""
    if not payload.items:
        return BaseApiOut(data={"created": 0, "skipped": 0})

    from core.tasks import create_task_id, register_task, complete_task, fail_task, send_task_progress

    task_id = create_task_id()
    register_task(task_id)

    async def _run_import():
        try:
            # Auto-create missing menus
            for menu_title in payload.create_menus:
                exists = await Menu.filter(title=menu_title).first()
                if not exists:
                    await Menu.create(title=menu_title, icon="ic:round-menu")

            # Pre-load menu map and existing titles for batch duplicate check
            all_menus = await Menu.all()
            menu_map = {m.title: m for m in all_menus}

            existing_titles = set()
            existing_links = await Links.filter(
                title__in=[item.title for item in payload.items if item.title]
            ).values_list("title", flat=True)
            existing_titles = set(existing_links)

            created = 0
            skipped = 0
            total = len(payload.items)

            for i, item in enumerate(payload.items):
                if not item.title or item.title in existing_titles:
                    skipped += 1
                else:
                    link = await Links.create(
                        title=item.title,
                        href=item.href,
                        icon=item.icon,
                        desc=item.desc,
                        color=item.color,
                        is_self=item.is_self,
                        is_vip=item.is_vip,
                        order=item.order,
                        cdn_img_id=item.cdn_img_id,
                        status=item.status,
                    )
                    menus_to_add = [menu_map[t] for t in item.menus if t in menu_map]
                    if menus_to_add:
                        await link.menus.add(*menus_to_add)
                    created += 1
                    existing_titles.add(item.title)

                # Send progress every 5 items or on last item
                if (i + 1) % 5 == 0 or (i + 1) == total:
                    await send_task_progress(task_id, {
                        "current": i + 1,
                        "total": total,
                        "created": created,
                        "skipped": skipped,
                    })

            await clear_link_cache()
            await complete_task(task_id, {"created": created, "skipped": skipped})
        except Exception as e:
            await fail_task(task_id, str(e))

    asyncio.create_task(_run_import())

    return BaseApiOut(data={"task_id": task_id})


@link_router.put("/{item_id}", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_link_update(item_id: str, item: CreateMenuSchema):
    await clear_link_cache()
    link = await Links.get_or_none(id=item_id)
    if not link:
        return not_found("链接")
    payload = item.model_dump(exclude_unset=True, exclude={"menus"})
    if payload:
        await Links.filter(id=item_id).update(**payload)
    if isinstance(item.menus, list):
        await link.menus.clear()
        await attach_link_menus(link, item.menus)
    return BaseApiOut()


@link_router.put("/update/all", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_link_update_all(items: list[LinkUpdateAllSchema]):
    await clear_link_cache()
    await update_links_batch(items)
    return BaseApiOut(message="批量更新成功")


@link_router.delete("/{item_ids}", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_link_delete(item_ids: str):
    ids = item_ids.split(",")
    await clear_link_cache()
    data = await Links.filter(id__in=ids).delete()
    return BaseApiOut(data=data)


@link_router.delete("/delete/all", response_model=BaseApiOut, dependencies=[Depends(get_current_super_user)])
async def handle_link_delete_all():
    await clear_link_cache()
    await Links.all().delete()
    return BaseApiOut(message="删除所有数据成功")


@link_router.post("/sync_cdn", dependencies=[Depends(get_current_user)])
async def handle_sync_cdn(link_id=None, url: str = ""):
    cdn_data = await sync_link_cdn(link_id, url)
    if not cdn_data:
        return BaseApiOut(code=400, message="同步CDN失败")
    return BaseApiOut(data=cdn_data)


@link_router.post("/sync_cdn_file", description="同步上传的文件", dependencies=[Depends(get_current_user)])
async def handle_sync_cdn_file(link_id=None, file: UploadFile = File(...)):
    cdn_data = await sync_link_cdn(link_id, await file.read())
    if not cdn_data:
        return BaseApiOut(code=400, message="同步CDN失败")
    return BaseApiOut(data=cdn_data)


@link_router.post("/siteinfo", dependencies=[Depends(get_current_user)])
async def handle_siteinfo(url: str):
    data = await get_site_info(url)
    if not data:
        return BaseApiOut(code=400, message="获取信息失败，请检查链接是否可访问")
    return BaseApiOut(data=data)


@link_router.post("/sync_cdn_batch", dependencies=[Depends(get_current_user)])
async def handle_sync_cdn_batch(link_ids: list[int]):
    """批量同步选中链接的图标到CDN（后台任务）"""
    if not link_ids:
        raise HTTPException(status_code=400, detail="请选择要同步的链接")

    from core.tasks import create_task_id, register_task, complete_task, fail_task

    task_id = create_task_id()
    register_task(task_id)

    async def _run_sync():
        try:
            result = await sync_links_cdn_batch(link_ids)
            await complete_task(task_id, result)
        except HTTPException as e:
            await fail_task(task_id, e.detail)
        except Exception as e:
            await fail_task(task_id, str(e))

    asyncio.create_task(_run_sync())

    return BaseApiOut(data={"task_id": task_id})


@link_router.get("/export", dependencies=[Depends(get_current_user)])
async def handle_link_export():
    """导出所有链接数据为JSON"""
    links = await Links.all().order_by("order").prefetch_related("menus")
    data = []
    for link in links:
        data.append({
            "title": link.title,
            "href": link.href,
            "icon": link.icon,
            "desc": link.desc,
            "color": link.color,
            "is_self": link.is_self,
            "is_vip": link.is_vip,
            "order": link.order,
            "cdn_img_id": link.cdn_img_id,
            "status": link.status,
            "menus": [m.title for m in link.menus],
        })
    content = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=links.json"},
    )


@link_router.post("/import", dependencies=[Depends(get_current_user)])
async def handle_link_import(file: UploadFile = File(...)):
    """从JSON文件导入链接数据"""
    content = await file.read()
    try:
        items = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON格式错误")
    if not isinstance(items, list):
        raise HTTPException(status_code=400, detail="数据格式错误，应为数组")

    # Pre-load menu map and existing titles for batch duplicate check
    all_menus = await Menu.all()
    menu_map = {m.title: m for m in all_menus}

    all_titles = [item.get("title") for item in items if item.get("title")]
    existing_links = await Links.filter(title__in=all_titles).values_list("title", flat=True)
    existing_titles = set(existing_links)

    created = 0
    skipped = 0
    for item in items:
        title = item.get("title")
        if not title or title in existing_titles:
            skipped += 1
            continue
        menu_titles = item.pop("menus", []) or []
        link = await Links.create(
            title=title,
            href=item.get("href", ""),
            icon=item.get("icon"),
            desc=item.get("desc"),
            color=item.get("color"),
            is_self=item.get("is_self", False),
            is_vip=item.get("is_vip", False),
            order=item.get("order", 0),
            cdn_img_id=item.get("cdn_img_id"),
            status=item.get("status", True),
        )
        menus_to_add = [menu_map[t] for t in menu_titles if t in menu_map]
        if menus_to_add:
            await link.menus.add(*menus_to_add)
        created += 1
        existing_titles.add(title)

    await clear_link_cache()
    return BaseApiOut(data={"created": created, "skipped": skipped})
