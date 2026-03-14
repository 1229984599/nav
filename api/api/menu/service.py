from typing import Any

from fastapi_cache import FastAPICache
from tortoise.transactions import in_transaction

from common.validation import parse_order_by as parse_order_by_with_whitelist
from common.validation import validate_batch_size as validate_batch_size_with_limit
from models import Menu
from .schemas import MenuSchemaUpdate, MenuUpdateAllSchema

MENU_ORDER_FIELDS = {
    "id",
    "title",
    "order",
    "color",
    "is_vip",
    "status",
    "parent_id",
    "create_time",
    "update_time",
}
MENU_BATCH_MAX_SIZE = 1000


async def clear_menu_cache() -> None:
    await FastAPICache.clear(namespace="menu")
    from .views import invalidate_tree_cache
    invalidate_tree_cache()


def parse_menu_order_by(order_by: str) -> list[str]:
    return parse_order_by_with_whitelist(order_by, MENU_ORDER_FIELDS, resource="菜单")


def normalize_parent_id(parent_id: Any) -> int | None:
    if parent_id in (None, "", 0, "0"):
        return None
    return int(parent_id)


def validate_menu_batch_size(items: list[Any], batch_name: str) -> None:
    validate_batch_size_with_limit(items, max_size=MENU_BATCH_MAX_SIZE, batch_name=batch_name)


async def create_menus_batch(items: list[MenuSchemaUpdate]) -> None:
    validate_menu_batch_size(items, "批量创建")
    async with in_transaction():
        menus = []
        for item in items:
            payload = item.model_dump(exclude_unset=True)
            payload["parent_id"] = normalize_parent_id(payload.pop("parent_id", None))
            menus.append(Menu(**payload))
        if menus:
            await Menu.bulk_create(menus, ignore_conflicts=False)


async def update_menus_batch(items: list[MenuUpdateAllSchema]) -> None:
    validate_menu_batch_size(items, "批量更新")
    async with in_transaction():
        for item in items:
            payload = item.model_dump(exclude_unset=True)
            item_id = payload.pop("id", None)
            if not item_id:
                continue
            if "parent_id" in payload:
                payload["parent_id"] = normalize_parent_id(payload["parent_id"])
            await Menu.filter(id=item_id).update(**payload)
