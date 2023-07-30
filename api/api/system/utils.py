from datetime import timedelta
from fastapi import  Security, HTTPException
from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearer, JwtAuthorizationCredentials, JwtRefreshBearerCookie

from core import settings
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

access_security = JwtAccessBearerCookie(
    secret_key=settings.SECRET_KEY,
    # auto_error=True,
    access_expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # change access token validation timedelta
)
# Read refresh token from bearer header only
refresh_security = JwtRefreshBearer(
    secret_key=settings.SECRET_KEY,
    # auto_error=True,  # automatically raise HTTPException: HTTP_401_UNAUTHORIZED
    refresh_expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password: 原密码
    :param hashed_password: hash后的密码
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    获取 hash 后的密码
    :param password:
    :return:
    """
    return pwd_context.hash(password)


async def get_current_user(credentials: JwtAuthorizationCredentials = Security(access_security)):
    user = await User.find_by_username(credentials['username'])
    # 当前用户是否存在
    if not user:
        raise HTTPException(status_code=419, detail='用户不存在，请检查是否登录')
    return user
