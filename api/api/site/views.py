from starlette.responses import FileResponse

from fastapi import APIRouter, Depends, UploadFile, File, Request
from models import Site
from core.crud import BaseApiOut
from .schemas import SiteSchemaUpdate
from core.auth import get_current_user
from settings import settings

site_router = APIRouter()


@site_router.post('/update', response_model=BaseApiOut[SiteSchemaUpdate])
async def handle_update_site(site: SiteSchemaUpdate, user=Depends(get_current_user)):
    """
    创更新数据
    """
    data = await Site.update_one(site.id, site.dict(exclude_unset=True, exclude={"id"}))
    data = await SiteSchemaUpdate.from_queryset_single(data)
    return BaseApiOut(data=data)


@site_router.get('/get', response_model=BaseApiOut)
async def handle_get_site():
    """
    获取数据站点
    """
    data = await Site.get_or_none(id=1)
    return BaseApiOut(data=data)


# 上传图片的路由和处理函数
@site_router.post("/upload/", response_model=BaseApiOut)
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
