from fastapi import APIRouter
from .user import user_router
from .menu import menu_router
from .nav import nav_router

api_router = APIRouter()

api_router.include_router(user_router, prefix='/user', tags=['用户管理'])
api_router.include_router(menu_router, prefix='/menu', tags=['菜单管理'])
api_router.include_router(nav_router, prefix='/nav', tags=['导航管理'])
