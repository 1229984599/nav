from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from auth import auth, schemas
from common.response import BaseApiOut
from core.http_status import HttpStatus
from models import User
from settings import settings

login_router = APIRouter()


@login_router.post("/login", name="Login", response_model=BaseApiOut[schemas.Token])
async def handle_login(form_data: schemas.LoginSchema):
    user = await User.filter(username=form_data.username, status=True).first()
    if not user:
        return BaseApiOut(code=HttpStatus.HTTP_419_USER_EXCEPT, message="用户不存在或已被禁用")
    if not auth.verify_password(form_data.password, user.password):
        return BaseApiOut(code=HttpStatus.HTTP_419_USER_EXCEPT, message="密码错误")
    subject = {"username": user.username}
    access_token = auth.access_security.create_access_token(subject=subject)
    refresh_token = auth.refresh_security.create_refresh_token(subject=subject)
    return BaseApiOut(
        message="登录成功",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token": access_token,
            "refreshToken": refresh_token,
            "expires": datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        },
    )


@login_router.post("/register", name="Register", response_model=BaseApiOut)
async def handle_register(form_data: schemas.RegisterSchema, _: User = Depends(auth.get_current_super_user)):
    user = await User.find_by_username(form_data.username)
    if user:
        return BaseApiOut(code=HttpStatus.HTTP_419_USER_EXCEPT, message="用户已存在")
    payload = form_data.model_dump()
    payload["password"] = auth.get_password_hash(payload["password"])
    data = await User.create(**payload)
    return BaseApiOut(data=data)


@login_router.post("/refresh", name="Refresh", response_model=BaseApiOut[schemas.Token])
async def refresh(credentials: JwtAuthorizationCredentials = Security(auth.refresh_security)):
    access_token = auth.access_security.create_access_token(subject=credentials.subject)
    refresh_token = auth.refresh_security.create_refresh_token(subject=credentials.subject)
    return BaseApiOut(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token": access_token,
            "refreshToken": refresh_token,
            "expires": datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
    )


@login_router.post("/refreshToken", name="RefreshToken")
async def refresh_token(credentials: JwtAuthorizationCredentials = Security(auth.refresh_security)):
    access_token = auth.access_security.create_access_token(subject=credentials.subject)
    new_refresh_token = auth.refresh_security.create_refresh_token(subject=credentials.subject)
    return BaseApiOut(
        data={
            "token": access_token,
            "refreshToken": new_refresh_token,
        }
    )


@login_router.get("/me", response_model=BaseApiOut[schemas.UserList])
async def read_current_user(user: User = Depends(auth.get_current_user)):
    data = schemas.UserList.model_validate(user, from_attributes=True)
    return BaseApiOut(data=data)


@login_router.get("/getUserInfo")
async def get_user_info(user: User = Depends(auth.get_current_user)):
    roles = ["super"] if user.is_super else ["user"]
    return BaseApiOut(data={
        "userId": str(user.id),
        "userName": user.username,
        "nickName": user.nickname or user.username,
        "roles": roles,
        "buttons": [],
    })


@login_router.put("/updateProfile")
async def update_profile(item: schemas.ProfileUpdate, user: User = Depends(auth.get_current_user)):
    payload = item.model_dump(exclude_unset=True)
    if payload:
        await User.filter(id=user.id).update(**payload)
    return BaseApiOut(message="更新成功")


@login_router.put("/changePassword")
async def change_password(item: schemas.ChangePassword, user: User = Depends(auth.get_current_user)):
    if not auth.verify_password(item.old_password, user.password):
        return BaseApiOut(code=HttpStatus.HTTP_419_USER_EXCEPT, message="旧密码错误")
    hashed = auth.get_password_hash(item.new_password)
    await User.filter(id=user.id).update(password=hashed)
    return BaseApiOut(message="密码修改成功")


@login_router.get("/getUserRoutes")
async def get_user_routes(user: User = Depends(auth.get_current_user)):
    routes = [
        {
            "name": "links",
            "path": "/links",
            "component": "layout.base$view.links",
            "meta": {"title": "链接管理", "icon": "pajamas:link", "order": 1},
        },
        {
            "name": "menu",
            "path": "/menu",
            "component": "layout.base$view.menu",
            "meta": {"title": "菜单管理", "icon": "ep:menu", "order": 2},
        },
        {
            "name": "friend",
            "path": "/friend",
            "component": "layout.base$view.friend",
            "meta": {"title": "友情链接", "icon": "fluent-mdl2:message-friend-request", "order": 3},
        },
        {
            "name": "system",
            "path": "/system",
            "component": "layout.base",
            "meta": {"title": "系统管理", "icon": "icon-park-outline:system", "order": 4},
            "children": [
                {
                    "name": "system_user",
                    "path": "/system/user",
                    "component": "view.system_user",
                    "meta": {"title": "用户列表", "icon": "mdi:user", "order": 1},
                },
                {
                    "name": "system_site",
                    "path": "/system/site",
                    "component": "view.system_site",
                    "meta": {"title": "站点设置", "icon": "dashicons:admin-site", "order": 2},
                },
            ],
        },
    ]

    if not user.is_super:
        routes = [r for r in routes if r["name"] != "system"]

    return BaseApiOut(data={
        "home": "links",
        "routes": routes,
    })
