from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from auth import auth, schemas
from common.errors import not_found
from common.response import BaseApiOut
from models import User

user_router = APIRouter()


@user_router.post("/list", response_model=BaseApiOut[Page[schemas.UserList]], dependencies=[Depends(auth.get_current_super_user)])
async def handle_user_list(filters: schemas.UserFilter, params: Params = Depends(), order_by: str = "-create_time"):
    query = User.all()
    filter_data = filters.model_dump(exclude_unset=True)
    if filter_data.get("status") is not None:
        query = query.filter(status=filter_data["status"])
    if filter_data.get("username"):
        query = query.filter(username__icontains=filter_data["username"])
    if order_by:
        query = query.order_by(*order_by.split(","))
    data = await paginate(query, params, True)
    return BaseApiOut(data=data)


@user_router.get("/read/{item_id}", response_model=BaseApiOut[schemas.UserList], dependencies=[Depends(auth.get_current_super_user)])
async def handle_user_read(item_id: str):
    item = await User.get_or_none(id=item_id)
    if not item:
        return not_found("用户")
    data = schemas.UserList.model_validate(item, from_attributes=True)
    return BaseApiOut(data=data)


@user_router.post("/create", response_model=BaseApiOut[schemas.UserList], dependencies=[Depends(auth.get_current_super_user)])
async def handle_user_create(item: schemas.UserCreate):
    payload = item.model_dump(exclude_unset=True)
    if payload.get("password"):
        payload["password"] = auth.get_password_hash(payload["password"])
    user = await User.create(**payload)
    data = schemas.UserList.model_validate(user, from_attributes=True)
    return BaseApiOut(data=data)


@user_router.post("/create/all", response_model=BaseApiOut, dependencies=[Depends(auth.get_current_super_user)])
async def handle_user_create_all(items: list[schemas.UserCreate]):
    users = []
    for item in items:
        payload = item.model_dump(exclude_unset=True)
        if payload.get("password"):
            payload["password"] = auth.get_password_hash(payload["password"])
        users.append(User(**payload))
    if users:
        await User.bulk_create(users, ignore_conflicts=False)
    return BaseApiOut(message="批量创建成功")


@user_router.put("/{item_id}", response_model=BaseApiOut, dependencies=[Depends(auth.get_current_super_user)])
async def handle_user_update(item_id: str, item: schemas.UserUpdate):
    user = await User.get_or_none(id=item_id)
    if not user:
        return not_found("用户")
    payload = item.model_dump(exclude_unset=True)

    # Username uniqueness check
    if "username" in payload and payload["username"]:
        existing = await User.filter(username=payload["username"]).exclude(id=item_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="用户名已被占用")

    # Last super user demotion protection
    if "is_super" in payload and payload["is_super"] is False and user.is_super:
        super_count = await User.filter(is_super=True).count()
        if super_count <= 1:
            raise HTTPException(status_code=400, detail="无法取消最后一个超级管理员的权限")

    if payload.get("password"):
        payload["password"] = auth.get_password_hash(payload["password"])
    data = await User.filter(id=item_id).update(**payload)
    return BaseApiOut(data=data)


@user_router.put("/update/all", response_model=BaseApiOut, dependencies=[Depends(auth.get_current_super_user)])
async def handle_user_update_all(items: list[schemas.UserUpdateAll]):
    for item in items:
        payload = item.model_dump(exclude_unset=True)
        item_id = payload.pop("id", None)
        if not item_id:
            continue

        # Username uniqueness check
        if "username" in payload and payload["username"]:
            existing = await User.filter(username=payload["username"]).exclude(id=item_id).first()
            if existing:
                raise HTTPException(status_code=400, detail=f"用户名 '{payload['username']}' 已被占用")

        # Last super user demotion protection
        if "is_super" in payload and payload["is_super"] is False:
            user = await User.get_or_none(id=item_id)
            if user and user.is_super:
                super_count = await User.filter(is_super=True).count()
                if super_count <= 1:
                    raise HTTPException(status_code=400, detail="无法取消最后一个超级管理员的权限")

        if payload.get("password"):
            payload["password"] = auth.get_password_hash(payload["password"])
        await User.filter(id=item_id).update(**payload)
    return BaseApiOut(message="批量更新成功")


@user_router.delete("/{item_ids}", response_model=BaseApiOut, dependencies=[Depends(auth.get_current_super_user)])
async def handle_user_delete(item_ids: str):
    ids = item_ids.split(",")
    # Prevent deleting the last super user
    super_users_being_deleted = await User.filter(id__in=ids, is_super=True).count()
    if super_users_being_deleted > 0:
        total_super_users = await User.filter(is_super=True).count()
        if total_super_users - super_users_being_deleted < 1:
            raise HTTPException(status_code=400, detail="无法删除最后一个超级管理员")
    data = await User.filter(id__in=ids).delete()
    return BaseApiOut(data=data)


@user_router.delete("/delete/all", response_model=BaseApiOut, dependencies=[Depends(auth.get_current_super_user)])
async def handle_user_delete_all():
    await User.all().delete()
    return BaseApiOut(message="删除所有数据成功")
