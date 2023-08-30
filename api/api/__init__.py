from fastapi import APIRouter
from .system import system_router
from .links import link_router
from .friend import friend_router
from .menu import menu_router
from .site import site_router
from .spider import spider_router

api_router = APIRouter()

api_router.include_router(system_router, prefix='/system')
api_router.include_router(link_router, prefix='/links', tags=['链接管理'])
api_router.include_router(friend_router, prefix='/friend', tags=['友情链接'])
api_router.include_router(menu_router, prefix='/menu', tags=['菜单管理'])
api_router.include_router(site_router, prefix='/site', tags=['站点管理'])
api_router.include_router(spider_router, prefix='/spider', tags=['爬虫管理'])
