from typing import Callable

from fastapi import Depends, HTTPException

from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate

from fastapi_tortoise_crud import ModelCrud, BaseApiOut
from models import Links, Menu, User
from .utils import get_site_info
from .schemas import CreateMenuSchema, LinkSchemaList, FilterSchemaList
from auth.auth import get_current_user, is_login


class LinkCrud(ModelCrud):

    @property
    def route_list(self) -> Callable:
        schema_filters = self.schema_filters

        async def route(filters: schema_filters,
                        params: Params = Depends(), order_by: str = '-create_time',
                        user: User = Depends(is_login)):
            queryset = self.model.filter()
            item = filters.model_dump(exclude_defaults=True)
            if item.get('menus'):
                menus = item.pop('menus')
                queryset = queryset.filter(menus__in=menus)
            if not user:
                queryset = queryset.filter(is_vip=False)
            if order_by:
                queryset = queryset.order_by(*order_by.split(','))
            search_item = {f'{k}__icontains': v for k, v in item.items() if v}
            queryset = queryset.filter(**search_item)
            data = await paginate(queryset, params, True)
            return BaseApiOut(data=data)

        return route

    @property
    def route_create(self) -> Callable:
        schema_create = self.schema_create

        async def route(item: schema_create):
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


@link_router.post('/siteinfo')
async def handle_siteinfo(url: str):
    data = await get_site_info(url)
    if not data:
        raise HTTPException(status_code=400, detail='获取信息失败')
    return BaseApiOut(data=data)
