from typing import Any

from tortoise.transactions import in_transaction

from common.validation import parse_order_by as parse_order_by_with_whitelist
from common.validation import validate_batch_size as validate_batch_size_with_limit
from models import Friend
from .schemas import FriendCreateSchema, FriendUpdateAllSchema

FRIEND_ORDER_FIELDS = {
    "id",
    "title",
    "href",
    "order",
    "status",
    "create_time",
    "update_time",
}
FRIEND_BATCH_MAX_SIZE = 1000


def parse_friend_order_by(order_by: str) -> list[str]:
    return parse_order_by_with_whitelist(order_by, FRIEND_ORDER_FIELDS, resource="友链")


def validate_friend_batch_size(items: list[Any], batch_name: str) -> None:
    validate_batch_size_with_limit(items, max_size=FRIEND_BATCH_MAX_SIZE, batch_name=batch_name)


async def create_friends_batch(items: list[FriendCreateSchema]) -> None:
    validate_friend_batch_size(items, "批量创建")
    async with in_transaction():
        friends = [Friend(**item.model_dump(exclude_unset=True)) for item in items]
        if friends:
            await Friend.bulk_create(friends, ignore_conflicts=False)


async def update_friends_batch(items: list[FriendUpdateAllSchema]) -> None:
    validate_friend_batch_size(items, "批量更新")
    async with in_transaction():
        for item in items:
            payload = item.model_dump(exclude_unset=True)
            item_id = payload.pop("id", None)
            if not item_id:
                continue
            await Friend.filter(id=item_id).update(**payload)
