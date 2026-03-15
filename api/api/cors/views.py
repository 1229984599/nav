from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from auth.auth import get_current_user
from common.errors import not_found
from common.response import BaseApiOut
from common.validation import parse_order_by as parse_order_by_with_whitelist
from core.middleware import load_cors_origins
from models import CorsOrigin
from .schemas import CorsCreateSchema, CorsFilterSchema, CorsListSchema, CorsUpdateAllSchema

cors_router = APIRouter()

CORS_ORDER_FIELDS = {"id", "origin", "order", "status", "create_time", "update_time"}


@cors_router.post("/list", response_model=BaseApiOut[Page[CorsListSchema]])
async def handle_cors_list(filters: CorsFilterSchema, params: Params = Depends(), order_by: str = "order"):
    query = CorsOrigin.all()
    item = filters.model_dump(exclude_unset=True)
    if item.get("origin"):
        query = query.filter(origin__icontains=item["origin"])
    if item.get("status") is not None:
        query = query.filter(status=item["status"])
    query = query.order_by(*parse_order_by_with_whitelist(order_by, CORS_ORDER_FIELDS, resource="跨域"))
    data = await paginate(query, params, True)
    return BaseApiOut(data=data)


@cors_router.post("/create", response_model=BaseApiOut[CorsCreateSchema], dependencies=[Depends(get_current_user)])
async def handle_cors_create(item: CorsCreateSchema):
    payload = item.model_dump(exclude_unset=True)
    created = await CorsOrigin.create(**payload)
    await load_cors_origins()
    return BaseApiOut(data=CorsCreateSchema.model_validate(created, from_attributes=True))


@cors_router.put("/{item_id}", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_cors_update(item_id: int, item: CorsCreateSchema):
    cors = await CorsOrigin.get_or_none(id=item_id)
    if not cors:
        return not_found("跨域配置")
    payload = item.model_dump(exclude_unset=True)
    await CorsOrigin.filter(id=item_id).update(**payload)
    await load_cors_origins()
    return BaseApiOut(data=1)


@cors_router.put("/update/all", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_cors_update_all(items: list[CorsUpdateAllSchema]):
    from tortoise.transactions import in_transaction
    async with in_transaction():
        for item in items:
            payload = item.model_dump(exclude_unset=True)
            item_id = payload.pop("id", None)
            if not item_id:
                continue
            await CorsOrigin.filter(id=item_id).update(**payload)
    await load_cors_origins()
    return BaseApiOut(message="批量更新成功")


@cors_router.delete("/{item_ids}", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_cors_delete(item_ids: str):
    ids = item_ids.split(",")
    data = await CorsOrigin.filter(id__in=ids).delete()
    await load_cors_origins()
    return BaseApiOut(data=data)
