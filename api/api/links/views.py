from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from auth.auth import get_current_user, is_login
from common.errors import not_found
from common.response import BaseApiOut
from models import Links, User
from .schemas import CreateMenuSchema, FilterSchemaList, LinkSchemaList, LinkUpdateAllSchema
from .service import (
    attach_link_menus,
    build_link_search_filters,
    clear_link_cache,
    create_links_batch,
    parse_order_by,
    sync_link_cdn,
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


@link_router.post("/create/all", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_link_create_all(items: list[CreateMenuSchema]):
    await clear_link_cache()
    await create_links_batch(items)
    return BaseApiOut(message="批量创建成功")


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


@link_router.delete("/{item_ids}", response_model=BaseApiOut)
async def handle_link_delete(item_ids: str):
    ids = item_ids.split(",")
    await clear_link_cache()
    data = await Links.filter(id__in=ids).delete()
    return BaseApiOut(data=data)


@link_router.delete("/delete/all", response_model=BaseApiOut)
async def handle_link_delete_all():
    await clear_link_cache()
    await Links.all().delete()
    return BaseApiOut(message="删除所有数据成功")


@link_router.post("/sync_cdn")
async def handle_sync_cdn(link_id=None, url: str = ""):
    cdn_data = await sync_link_cdn(link_id, url)
    if not cdn_data:
        return BaseApiOut(code=400, message="同步CDN失败")
    return BaseApiOut(data=cdn_data)


@link_router.post("/sync_cdn_file", description="同步上传的文件")
async def handle_sync_cdn_file(link_id=None, file: UploadFile = File(...)):
    cdn_data = await sync_link_cdn(link_id, await file.read())
    if not cdn_data:
        return BaseApiOut(code=400, message="同步CDN失败")
    return BaseApiOut(data=cdn_data)


@link_router.post("/siteinfo")
async def handle_siteinfo(url: str):
    data = await get_site_info(url)
    if not data:
        return BaseApiOut(code=400, message="获取信息失败，请检查链接是否可访问")
    return BaseApiOut(data=data)
