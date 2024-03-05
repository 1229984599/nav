from typing import Callable

from fastapi_cache import FastAPICache
from fastapi import Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse

from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate

from fastapi_tortoise_crud import ModelCrud, BaseApiOut
from models import Links, Menu, User, Site
from .utils import get_site_info, CdnImg, ignore_async_errors
from .schemas import CreateMenuSchema, LinkSchemaList, FilterSchemaList
from auth.auth import get_current_user, is_login


class LinkCrud(ModelCrud):

    @property
    def route_list(self) -> Callable:
        schema_filters = self.schema_filters

        async def route(filters: schema_filters,
                        params: Params = Depends(), order_by: str = '-create_time',
                        user: User = Depends(is_login)):
            item = await self.pre_list(filters)
            queryset = self.model.filter()
            # item = filters.model_dump(exclude_defaults=True)
            if item.get('menus'):
                menus = item.pop('menus')
                queryset = queryset.filter(menus__in=menus)
            if not user:
                queryset = queryset.filter(is_vip=False)
            if order_by:
                queryset = queryset.order_by(*order_by.split(','))
            # search_item = {f'{k}__icontains': v for k, v in item.items() if v}
            queryset = queryset.filter(**item)
            data = await paginate(queryset, params, True)
            return BaseApiOut(data=data)

        return route

    @property
    def route_create(self) -> Callable:
        schema_create = self.schema_create

        async def route(item: schema_create):
            # 清除链接缓存
            await FastAPICache.clear()
            data = item.dict(exclude_unset=True, exclude={'menus'})
            pass
            link = await self.model.create(**data)
            if item.menus:
                menus = await Menu.filter(id__in=item.menus)
                await link.menus.add(*menus)

            return BaseApiOut(data=data)

        return route

    @property
    def route_update(self) -> Callable:
        schema_update = self.schema_update

        async def route(item_id: str, item: schema_update):
            # 清除链接缓存
            await FastAPICache.clear()
            link = await self.model.get_or_none(id=item_id)
            if not link:
                return BaseApiOut(code=400, message='链接不存在')
            data_dict = item.dict(exclude_unset=True, exclude={'menus'})
            if data_dict:
                updated_item = await self.model.filter(id=item_id).update(**data_dict)
            pass
            # 如果需要更新菜单
            if isinstance(item.menus, list):
                await link.menus.clear()
                # 删除关联
                menus = await Menu.filter(id__in=item.menus)
                await link.menus.add(*menus)
            return BaseApiOut()

        return route


link_router = LinkCrud(Links,
                       schema_list=LinkSchemaList,
                       schema_create=CreateMenuSchema,
                       schema_update=CreateMenuSchema,
                       schema_filters=FilterSchemaList
                       ).register_crud(
    depends_create=[Depends(get_current_user)],
    depends_update=[Depends(get_current_user)]
)


@ignore_async_errors
async def handle_link_sync(link_id, url: str | bytes):
    """
    处理链接同步
    :param url: url地址或者file对象
    :param link_id: 链接id（存储于数据库中）
    :return:
    """
    data = await Site.first()
    if not data.cdn_img_token:
        return BaseApiOut(code=400, message='未配置图床token')
    spider = CdnImg(data.cdn_img_token)
    # 上传图片
    cdn_data = await spider.upload_img(url)
    # 通过id查找当前链接
    link_model = await Links.find_one(id=link_id)
    # 删除以前连接存在的图片
    if link_model.cdn_img_id:
        await spider.delete_img(link_model.cdn_img_id)
    # 更新当前重新上传的cdn链接（防止有人上传后不保存）
    link_model.update_from_dict({
        'cdn_img_id': cdn_data.get('id'),
        'icon': cdn_data.get('url'),
    })
    await link_model.save()
    return cdn_data


@link_router.post('/sync_cdn')
async def handle_sync_cdn(link_id, url: str):
    cdn_data = await handle_link_sync(link_id, url)
    if not cdn_data:
        return JSONResponse(status_code=400, content='同步CDN失败')
    return BaseApiOut(data=cdn_data)
    pass


@link_router.post('/sync_cdn_file', description='同步上传的文件')
async def handle_sync_cdn_file(link_id, file: UploadFile = File(...)):
    cdn_data = await handle_link_sync(link_id, file.file.read())
    if not cdn_data:
        return JSONResponse(status_code=400, content='同步CDN失败')
    return BaseApiOut(data=cdn_data)
    pass


@link_router.post('/siteinfo')
async def handle_siteinfo(url: str):
    data = await get_site_info(url)
    if not data:
        raise HTTPException(status_code=400, detail='获取信息失败')
    return BaseApiOut(data=data)
