from fastapi_cache import FastAPICache

from fastapi_cache.decorator import cache

from starlette.responses import FileResponse
from fastapi import APIRouter, Depends, UploadFile, File, Request
from fastapi_tortoise_crud import BaseApiOut

from models import Site
from .schemas import SiteSchemaUpdate
from auth.auth import get_current_user
from settings import settings

site_router = APIRouter()


@site_router.post('/update', response_model=BaseApiOut[SiteSchemaUpdate], dependencies=[Depends(get_current_user)])
async def handle_update_site(site: SiteSchemaUpdate):
    """
    创更新数据
    """
    first_model = await Site.first()
    await first_model.update_from_dict(site.dict(exclude_unset=True, exclude={"id"}))
    await first_model.save()
    # data = await Site.update_one(site.id, site.dict(exclude_unset=True, exclude={"id"}))
    # site_info = await Site.get_or_none(id=data)
    data = await SiteSchemaUpdate.from_tortoise_orm(first_model)
    # 清除链接缓存
    await FastAPICache.clear(namespace='site')
    return BaseApiOut(data=data)


@site_router.get('/get', response_model=BaseApiOut)
# 站点数据，几乎不会改变，缓存30天
@cache(expire=60 * 60 * 24 * 30, namespace='site')
async def handle_get_site():
    """
    获取数据站点
    """
    data = await Site.first()
    data = await Site.schema_list().from_tortoise_orm(data)
    return BaseApiOut(data=data)


# 上传图片的路由和处理函数
@site_router.post("/upload/", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def upload_image(request: Request, file: UploadFile = File(...)):
    img_path = settings.BASE_PATH.joinpath('img').joinpath('logo.png')
    with open(img_path, "wb") as f:
        f.write(file.file.read())
    img_url = f"{request.base_url}api/site/get_image/logo.png"
    return BaseApiOut(data={"img_url": img_url})


# 访问图片的路由和处理函数
@site_router.get("/get_image/{filename}")
async def get_image(filename: str):
    img_path = settings.BASE_PATH.joinpath('img').joinpath(filename)
    return FileResponse(img_path)


@site_router.post('/clear_cache')
async def handle_clear_cache():
    """
    清除缓存
    """
    data = await FastAPICache.clear()
    return BaseApiOut(message='缓存清除成功')
