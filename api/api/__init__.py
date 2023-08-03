from fastapi import APIRouter
from .system import user_router, login_router
from .menu import menu_router
from .links import link_router
from .site import site_router
from .friend import friend_router

api_router = APIRouter()

api_router.include_router(login_router, prefix='/login', tags=['登录管理'])
api_router.include_router(user_router, prefix='/user', tags=['用户管理'])
api_router.include_router(menu_router, prefix='/menu', tags=['菜单管理'])
api_router.include_router(link_router, prefix='/link', tags=['链接管理'])
api_router.include_router(site_router, prefix='/site', tags=['站点管理'])
api_router.include_router(friend_router, prefix='/friend', tags=['友情链接'])
