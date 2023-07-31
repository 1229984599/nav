from datetime import timedelta, datetime

from fastapi import APIRouter, Security, Request, Depends
from fastapi_jwt import JwtAuthorizationCredentials
from core.crud import BaseApiOut

from .schemas import UserRead, Token
from .utils import verify_password, get_password_hash, get_current_user, access_security, refresh_security
from models import User
from settings import settings

login_router = APIRouter()


@login_router.post("/login", name='Login', response_model=BaseApiOut[Token])
async def handle_login(form_data: User.schema_create(name='Login', include=('username', 'password'))):
    user = await User.find_by_username(form_data.username)
    if not user:
        return BaseApiOut(code=419, message='用户不存在')
    if not verify_password(form_data.password, user.password):
        return BaseApiOut(code=419, message='密码错误')
    subject = {
        'username': user.username,
    }
    # Create new access/refresh tokens pair
    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject, )
    return BaseApiOut(
        message='登录成功',
        data={"access_token": access_token,
              "refresh_token": refresh_token,
              'expires': datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
              })
    # return {"access_token": access_token, "refresh_token": refresh_token}


@login_router.post("/register", name='Register', response_model=BaseApiOut)
async def handle_register(form_data: User.schema_create(name='Register', include=('username', 'password', 'nickname'))):
    user = await User.find_by_username(form_data.username)
    if user:
        return BaseApiOut(code=419, message='用户已存在')
    form_data.password = get_password_hash(form_data.password)
    data = await User.create_one(form_data.dict())
    return BaseApiOut(data=data)


@login_router.post("/refresh", name='Refresh', response_model=BaseApiOut[Token])
async def refresh(
        credentials: JwtAuthorizationCredentials = Security(refresh_security)
):
    # Update access/refresh tokens pair
    # We can customize expires_delta when creating
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject)

    return BaseApiOut(data={"access_token": access_token, "refresh_token": refresh_token,
                            'expires': datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)})
    # return {"access_token": access_token, "refresh_token": refresh_token}


@login_router.get("/users/me", response_model=BaseApiOut[UserRead])
async def read_current_user(user: User = Depends(get_current_user)):
    user = await UserRead.from_tortoise_orm(user)
    return BaseApiOut(data=user)
