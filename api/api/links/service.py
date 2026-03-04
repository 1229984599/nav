from typing import Any

from fastapi import HTTPException
from fastapi_cache import FastAPICache
from loguru import logger
from tortoise.transactions import in_transaction

from common.validation import parse_order_by as parse_order_by_with_whitelist
from common.validation import validate_batch_size as validate_batch_size_with_limit
from models import Links, Menu, Site
from .schemas import CreateMenuSchema, LinkSchemaList, LinkUpdateAllSchema
from .utils import CdnImg

LINK_TEXT_FILTER_FIELDS = {"title", "href"}
LINK_ORDER_FIELDS = {
    "id",
    "title",
    "href",
    "is_self",
    "is_vip",
    "order",
    "status",
    "create_time",
    "update_time",
}
LINK_BATCH_MAX_SIZE = 1000


async def clear_link_cache() -> None:
    await FastAPICache.clear()


def build_link_search_filters(item: dict[str, Any]) -> dict[str, Any]:
    search_item: dict[str, Any] = {}
    for key, value in item.items():
        if value or isinstance(value, bool):
            if isinstance(value, str) and key in LINK_TEXT_FILTER_FIELDS:
                search_item[f"{key}__icontains"] = value
            else:
                search_item[key] = value
    return search_item


def parse_order_by(order_by: str) -> list[str]:
    return parse_order_by_with_whitelist(order_by, LINK_ORDER_FIELDS, resource="链接")


async def load_menu_map(menu_ids: set[int]) -> dict[int, Menu]:
    if not menu_ids:
        return {}
    menus = await Menu.filter(id__in=list(menu_ids))
    return {menu.id: menu for menu in menus}


def validate_batch_size(items: list[Any], batch_name: str) -> None:
    validate_batch_size_with_limit(items, max_size=LINK_BATCH_MAX_SIZE, batch_name=batch_name)


async def attach_link_menus(link: Links, menu_ids: list[int] | None) -> None:
    if not menu_ids:
        return
    menus = await Menu.filter(id__in=menu_ids)
    if menus:
        await link.menus.add(*menus)


async def create_links_batch(items: list[CreateMenuSchema]) -> None:
    validate_batch_size(items, "批量创建")
    menu_id_set: set[int] = set()
    for item in items:
        if item.menus:
            menu_id_set.update(item.menus)
    menu_map = await load_menu_map(menu_id_set)

    async with in_transaction():
        for item in items:
            payload = item.model_dump(exclude_unset=True, exclude={"menus"})
            link = await Links.create(**payload)
            if item.menus:
                menus = [menu_map[menu_id] for menu_id in item.menus if menu_id in menu_map]
                if menus:
                    await link.menus.add(*menus)


async def update_links_batch(items: list[LinkUpdateAllSchema]) -> None:
    validate_batch_size(items, "批量更新")
    item_payloads: list[dict[str, Any]] = []
    link_ids: list[int] = []
    menu_id_set: set[int] = set()

    for item in items:
        payload = item.model_dump(exclude_unset=True)
        item_id = payload.get("id")
        if not item_id:
            continue
        link_ids.append(item_id)
        menus = payload.get("menus")
        if isinstance(menus, list):
            menu_id_set.update(menus)
        item_payloads.append(payload)

    link_map = {link.id: link for link in await Links.filter(id__in=link_ids)}
    menu_map = await load_menu_map(menu_id_set)

    async with in_transaction():
        for payload in item_payloads:
            item_id = payload.pop("id")
            menus = payload.pop("menus", None)
            if payload:
                await Links.filter(id=item_id).update(**payload)
            if isinstance(menus, list) and item_id in link_map:
                link = link_map[item_id]
                await link.menus.clear()
                new_menus = [menu_map[mid] for mid in menus if mid in menu_map]
                if new_menus:
                    await link.menus.add(*new_menus)


async def sync_link_cdn(link_id, url: str | bytes):
    site = await Site.first()
    if not site or not site.cdn_img_token:
        raise HTTPException(status_code=400, detail="未配置图床token")

    spider = CdnImg(site.cdn_img_token)
    cdn_data = await spider.upload_img(url)
    if not link_id:
        return cdn_data

    link_model = await Links.get_or_none(id=link_id)
    if link_model and link_model.cdn_img_id:
        await spider.delete_img(link_model.cdn_img_id)
    if link_model:
        link_model.update_from_dict({"cdn_img_id": cdn_data.get("id"), "icon": cdn_data.get("url")})
        await link_model.save()
    return cdn_data


async def sync_links_cdn_batch(link_ids: list[int]) -> dict:
    """批量将选中链接的图标同步到CDN"""
    if not link_ids:
        raise HTTPException(status_code=400, detail="请选择要同步的链接")

    site = await Site.first()
    if not site or not site.cdn_img_token:
        raise HTTPException(status_code=400, detail="未配置图床token")

    links = await Links.filter(id__in=link_ids)
    if not links:
        raise HTTPException(status_code=400, detail="未找到指定的链接")

    spider = CdnImg(site.cdn_img_token)
    success_count = 0
    fail_count = 0
    fail_items = []

    for link in links:
        if not link.icon:
            fail_count += 1
            fail_items.append({"id": link.id, "title": link.title, "reason": "没有图标地址"})
            continue
        try:
            # 如果已有CDN图片，先删除旧的
            if link.cdn_img_id:
                try:
                    await spider.delete_img(link.cdn_img_id)
                except Exception:
                    pass

            cdn_data = await spider.upload_img(link.icon)
            if cdn_data:
                link.update_from_dict({"cdn_img_id": cdn_data.get("id"), "icon": cdn_data.get("url")})
                await link.save()
                success_count += 1
            else:
                fail_count += 1
                fail_items.append({"id": link.id, "title": link.title, "reason": "上传失败"})
        except Exception as e:
            fail_count += 1
            fail_items.append({"id": link.id, "title": link.title, "reason": str(e)})
            logger.warning(f"CDN同步失败 link_id={link.id}: {e}")

    if success_count > 0:
        await clear_link_cache()

    return {
        "total": len(links),
        "success": success_count,
        "fail": fail_count,
        "fail_items": fail_items,
    }
