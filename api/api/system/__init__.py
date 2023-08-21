from fastapi import APIRouter
from .login import login_router
from .user import user_router


system_router = APIRouter()
system_router.include_router(login_router, prefix='/login', tags=['登录管理'])
system_router.include_router(user_router, prefix='/user', tags=['用户管理'])
