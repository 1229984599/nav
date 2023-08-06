from typing import Callable

from fastapi import Depends

from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate

from core.crud import ModelCrud, BaseApiOut
from models import Links, Menu, User
from .utils import get_site_info
from .schemas import CreateMenuSchema, SetMenuSchema, LinkSchemaList, UpdateMenuSchema, FilterSchemaList
from core.auth import get_current_user, is_login


class LinkCrud(ModelCrud):

    @property
    def route_list(self) -> Callable:
        schema_filters = self.schema_filters

        async def route(filters: schema_filters,
                        params: Params = Depends(), order_by: str = '-create_time',
                        user: User = Depends(is_login)):
            queryset = self.model.filter(is_delete=False)
            item = filters.dict(exclude_defaults=True)
            if item.get('menus'):
                menus = item.pop('menus')
                queryset = queryset.filter(menus__in=menus)
            if not user:
                queryset = queryset.filter(is_vip=False)
            queryset = await self.pre_list(queryset, item)
            if order_by:
                queryset = queryset.order_by(*order_by.split(','))
            data = await paginate(queryset, params, True)
            return BaseApiOut(data=data)

        return route


link_router = LinkCrud(Links,
                       schema_list=LinkSchemaList,
                       schema_filters=FilterSchemaList
                       ).register_crud(
    depends_create=[Depends(get_current_user)],
    depends_update=[Depends(get_current_user)]
)


@link_router.post('/menu/create', response_model=BaseApiOut)
async def handle_create(createSchema: CreateMenuSchema):
    """
    创建导航菜单
    """
    data = createSchema.dict(exclude_unset=True, exclude={'menus'})
    pass
    link = await Links.create(**data)
    if createSchema.menus:
        menus = await Menu.filter(id__in=createSchema.menus)
        await link.menus.add(*menus)
    return BaseApiOut(data=data)


@link_router.put("/menu/{item_id}", response_model=BaseApiOut)
async def handle_update(item_id: str, item: UpdateMenuSchema):
    link = await Links.get_or_none(id=item_id)
    if not link:
        return BaseApiOut(code=400, message='链接不存在')
    data_dict = item.dict(exclude_unset=True, exclude={'menus'})
    if data_dict:
        updated_item = await Links.filter(id=item_id).update(**data_dict)
    pass
    # 如果需要更新菜单
    if isinstance(item.menus, list):
        await link.menus.clear()
        # 删除关联
        menus = await Menu.filter(id__in=item.menus)
        await link.menus.add(*menus)

    # data = await UpdateMenuSchema.from_queryset_single(updated_item)
    return BaseApiOut()


@link_router.post('/siteinfo')
async def handle_siteinfo(url: str):
    data = await get_site_info(url)
    return BaseApiOut(data=data)


@link_router.post('/set_menu')
async def handle_set_menu(set_menu: SetMenuSchema):
    """
    设置链接菜单
    """
    link = await Links.find_one(id=set_menu.link_id)
    if not link:
        return BaseApiOut(code=400, message='导航不存在')
    menus = await Menu.filter(id__in=set_menu.menus).all()
    if not menus:
        return BaseApiOut(code=400, message='菜单不存在')
    await link.menus.clear()
    await link.menus.add(*menus)
    return BaseApiOut(message='设置导航菜单成功')
