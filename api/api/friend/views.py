from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from auth.auth import get_current_user
from common.errors import not_found
from common.response import BaseApiOut
from models import Friend
from .schemas import FriendCreateSchema, FriendFilterSchema, FriendListSchema, FriendUpdateAllSchema
from .service import create_friends_batch, parse_friend_order_by, update_friends_batch
from ..links.utils import get_site_info


friend_router = APIRouter()


@friend_router.post("/list", response_model=BaseApiOut[Page[FriendListSchema]])
async def handle_friend_list(filters: FriendFilterSchema, params: Params = Depends(), order_by: str = "-create_time"):
    query = Friend.all()
    item = filters.model_dump(exclude_unset=True)
    if item.get("title"):
        query = query.filter(title__icontains=item["title"])
    if item.get("status") is not None:
        query = query.filter(status=item["status"])
    query = query.order_by(*parse_friend_order_by(order_by))
    data = await paginate(query, params, True)
    return BaseApiOut(data=data)


@friend_router.get("/read/{item_id}", response_model=BaseApiOut[FriendListSchema])
async def handle_friend_read(item_id: str):
    item = await Friend.get_or_none(id=item_id)
    if not item:
        return not_found("友链")
    return BaseApiOut(data=FriendListSchema.model_validate(item, from_attributes=True))


@friend_router.post("/create", response_model=BaseApiOut[FriendCreateSchema], dependencies=[Depends(get_current_user)])
async def handle_friend_create(item: FriendCreateSchema):
    payload = item.model_dump(exclude_unset=True)
    created = await Friend.create(**payload)
    return BaseApiOut(data=FriendCreateSchema.model_validate(created, from_attributes=True))


@friend_router.post("/create/all", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_friend_create_all(items: list[FriendCreateSchema]):
    await create_friends_batch(items)
    return BaseApiOut(message="批量创建成功")


@friend_router.put("/{item_id}", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_friend_update(item_id: str, item: FriendCreateSchema):
    friend = await Friend.get_or_none(id=item_id)
    if not friend:
        return not_found("友链")
    payload = item.model_dump(exclude_unset=True)
    data = await Friend.filter(id=item_id).update(**payload)
    return BaseApiOut(data=data)


@friend_router.put("/update/all", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_friend_update_all(items: list[FriendUpdateAllSchema]):
    await update_friends_batch(items)
    return BaseApiOut(message="批量更新成功")


@friend_router.delete("/{item_ids}", response_model=BaseApiOut)
async def handle_friend_delete(item_ids: str):
    ids = item_ids.split(",")
    data = await Friend.filter(id__in=ids).delete()
    return BaseApiOut(data=data)


@friend_router.delete("/delete/all", response_model=BaseApiOut)
async def handle_friend_delete_all():
    await Friend.all().delete()
    return BaseApiOut(message="删除所有数据成功")


@friend_router.post('/siteinfo')
async def handle_siteinfo(url: str):
    data = await get_site_info(url)
    return BaseApiOut(data=data)
