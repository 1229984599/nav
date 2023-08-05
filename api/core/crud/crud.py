from typing import Union, Any, List, Callable
from fastapi import APIRouter, Depends
from tortoise.contrib.pydantic import PydanticModel
from tortoise.queryset import QuerySet
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from ..db import BaseModel
from .response import BaseApiOut


class PreMixin:
    @classmethod
    def pre_create(cls, item: PydanticModel) -> dict:
        return item.dict()

    @classmethod
    def pre_create_all(cls, items: list):
        for item in items:
            yield cls.pre_create(item.dict())

    @classmethod
    async def pre_update(cls, item: PydanticModel, item_id=None) -> dict:
        return item.dict(exclude_unset=True)

    @classmethod
    async def pre_list(cls, queryset: QuerySet, item: dict) -> QuerySet:
        """
        数据预处理：搜索字段
        :param queryset:
        :param item:
        :return:
        """
        filter_field = {f'{k}__icontains': v for k, v in item.items() if v}
        return queryset.filter(**filter_field)


class ModelCrud(APIRouter, PreMixin):
    def __init__(self, model: Union[BaseModel, Any],
                 schema_list=None,
                 schema_create=None,
                 schema_read=None,
                 schema_update=None,
                 schema_delete=None,
                 schema_filters=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.schema_list = schema_list or model.schema_list()
        self.schema_read = schema_read or model.schema_read()
        self.schema_update = schema_update or model.schema_update()
        self.schema_create = schema_create or model.schema_create()
        self.schema_delete = schema_delete or model.schema_delete()
        self.schema_filters = schema_filters or model.schema_filters()

    @property
    def route_list(self) -> Callable:
        schema_filters = self.schema_filters

        async def route(filters: schema_filters, params: Params = Depends(), order_by: str = '-create_time'):
            queryset = self.model.filter(is_delete=False)
            queryset = await self.pre_list(queryset, filters.dict(exclude_defaults=True))
            if order_by:
                queryset = queryset.order_by(*order_by.split(','))
            data = await paginate(queryset, params, True)
            return BaseApiOut(data=data)

        return route

    @property
    def route_read(self) -> Callable:
        async def route(item_id):
            data = await self.model.find_one(id=item_id)
            data = await self.schema_read.from_tortoise_orm(data)
            return BaseApiOut(data=data)

        return route

    @property
    def route_create(self) -> Callable:
        schema_create = self.schema_create

        async def route(item: schema_create):
            item = self.pre_create(item)
            new_item = await self.model.create_one(item)
            data = await self.schema_create.from_tortoise_orm(new_item)
            return BaseApiOut(data=data)

        return route

    @property
    def route_create_all(self) -> Callable:
        schema_create = self.schema_create

        async def route(items: List[schema_create]):
            items = self.pre_create_all(items)
            await self.model.bulk_create([self.model(**item) for item in items], ignore_conflicts=True)
            return BaseApiOut(message='批量创建成功')

        return route

    @property
    def route_update(self) -> Callable:
        schema_update = self.schema_update

        async def route(item_id: str, item: schema_update):
            item = await self.pre_update(item, item_id=item_id)
            updated_item = await self.model.update_one(item_id, item)
            data = await schema_update.from_queryset_single(updated_item)
            return BaseApiOut(data=data)

        return route

    @property
    def route_update_all(self) -> Callable:
        schema_update = self.schema_update

        async def route(items: List[schema_update]):
            for item in items:
                await self.route_update()(item.id, item)
            return BaseApiOut(message='批量更新成功')

        return route

    @property
    def route_delete(self) -> Callable:
        async def route(item_ids: str):
            ids = item_ids.split(',')
            data = await self.model.delete_many(ids)
            return BaseApiOut(data=data)

        return route

    def register_crud(self,
                      depends_list: List[Depends] = None,
                      depends_create: List[Depends] = None,
                      depends_update: List[Depends] = None,
                      depends_delete: List[Depends] = None,
                      ):
        model_name = self.model.__name__.lower()

        self.add_api_route(
            '/list',
            self.route_list,
            methods=['POST'],
            response_model=BaseApiOut[Page[self.schema_list]],
            name=f'{model_name}Read',
            summary=f'{model_name} List',
            dependencies=depends_list
        )
        self.add_api_route(
            '/read/{item_id}',
            self.route_read,
            methods=['GET'],
            response_model=BaseApiOut[self.schema_read],
            name=f'{model_name}Read',
            summary=f'{model_name} Read',
            dependencies=depends_list
        )

        self.add_api_route(
            '/create',
            self.route_create,
            methods=['POST'],
            response_model=BaseApiOut[self.schema_create],
            name=f'{model_name}Create',
            summary=f'{model_name} Create',
            dependencies=depends_create
        )

        self.add_api_route(
            '/create/all',
            self.route_create_all,
            methods=['POST'],
            response_model=BaseApiOut,
            name=f'{model_name}Create',
            summary=f'{model_name} CreateAll',
            dependencies=depends_create
        )

        self.add_api_route(
            '/{item_id}',
            self.route_update,
            methods=['PUT'],
            response_model=BaseApiOut[self.schema_update],
            name=f'{model_name}Update',
            summary=f'{model_name} Update',
            dependencies=depends_update
        )
        self.add_api_route(
            '/update/all',
            self.route_update_all,
            methods=['PUT'],
            response_model=BaseApiOut,
            name=f'{model_name}Update',
            summary=f'{model_name} UpdateAll',
            dependencies=depends_update
        )

        self.add_api_route(
            '/{item_ids}',
            self.route_delete,
            methods=['DELETE'],
            response_model=BaseApiOut,
            description='删除1条或多条数据example：1,2',
            name=f'{model_name}Delete',
            summary=f'{model_name} Delete',
            dependencies=depends_delete
        )
        return self


__all__ = [
    'ModelCrud'
]
