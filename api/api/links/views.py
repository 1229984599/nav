from tortoise.queryset import QuerySet

from core.crud import ModelCrud, BaseApiOut
from models import Links, Menu
from .utils import get_site_info
from .schemas import CreateMenuSchema, SetMenuSchema, LinkSchemaList, UpdateMenuSchema, FilterSchemaList


class LinkCrud(ModelCrud):
    @classmethod
    def pre_list(cls, queryset: QuerySet, item: dict) -> QuerySet:
        if item.get('menus'):
            menus = item.pop('menus')
            queryset = queryset.filter(menus__in=menus)
        return super().pre_list(queryset, item)


link_router = LinkCrud(Links,
                       schema_list=LinkSchemaList,
                       schema_filters=FilterSchemaList
                       ).register_crud()


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
        return BaseApiOut(code=400, message='导航不存在')
    updated_item = await Links.filter(id=item_id).update(**item.dict(exclude_unset=True, exclude={'menus'}))
    pass
    if item.menus:
        await link.menus.clear()
        # 删除关联
        menus = await Menu.filter(id__in=item.menus)
        await link.menus.add(*menus)
    # data = await UpdateMenuSchema.from_queryset_single(updated_item)
    return BaseApiOut(data=updated_item)


@link_router.post('/siteinfo')
async def handle_sietinfo(url: str):
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
