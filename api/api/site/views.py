from fastapi import APIRouter
from models import Site
from core.crud import BaseApiOut
from .schemas import SiteSchemaList, SiteSchemaUpdate

site_router = APIRouter()


@site_router.post('/update', response_model=BaseApiOut[SiteSchemaUpdate])
async def handle_update_site(site: SiteSchemaUpdate):
    """
    创建或者更新数据
    """
    if site.id:
        data = await Site.update_one(site.id, site.dict(exclude_unset=True, exclude={"id"}))
        data = await SiteSchemaUpdate.from_queryset_single(data)
        return BaseApiOut(data=data)
    else:
        await Site.create_one(site.dict(exclude_unset=True, exclude={"id"}))
        data = await Site.get(id=1)
    data = await SiteSchemaUpdate.from_tortoise_orm(data)
    return BaseApiOut(data=data)


@site_router.get('/get', response_model=BaseApiOut)
async def handle_get_site():
    """
    获取数据
    """
    data = await Site.get_or_none(id=1)
    return BaseApiOut(data=data)
