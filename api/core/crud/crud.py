from typing import Union, Any, List
from fastapi import APIRouter, Depends
from tortoise.contrib.pydantic import PydanticModel
from tortoise.queryset import QuerySet
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from ..db import BaseModel
from .response import BaseApiOut


class ModelCrud(APIRouter):
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
    def pre_list(cls, queryset: QuerySet, item: dict) -> QuerySet:
        """
        数据预处理：搜索字段
        :param queryset:
        :param item:
        :return:
        """
        filter_field = {f'{k}__icontains': v for k, v in item.items() if v}
        return queryset.filter(**filter_field)

    def register_crud(self,
                      depends_list: List[Depends] = None,
                      depends_create: List[Depends] = None,
                      depends_update: List[Depends] = None,
                      depends_delete: List[Depends] = None,
                      ):
        model_name = self.model.__name__.lower()
        schema_create = self.schema_create
        schema_update = self.schema_update
        schema_filters = self.schema_filters

        @self.post('/list', response_model=BaseApiOut[Page[self.schema_list]], name=f'{model_name}Read',
                   summary=f'{model_name} List',
                   dependencies=depends_list)
        async def handle_list(filters: schema_filters, params: Params = Depends(), order_by: str = '-created'):
            queryset = self.model.filter(is_delete=False)
            queryset = self.pre_list(queryset, filters.dict(exclude_defaults=True))
            queryset = queryset.order_by(order_by)
            data = await paginate(queryset, params, True)
            return BaseApiOut(data=data)

        @self.get('/read/{item_id}', response_model=BaseApiOut[self.schema_read], name=f'{model_name}Read',
                  summary=f'{model_name} Read',
                  dependencies=depends_list)
        async def handle_read(item_id):
            data = await self.model.find_one(id=item_id)
            data = await self.schema_read.from_tortoise_orm(data)
            return BaseApiOut(data=data)

        @self.post("/create", response_model=BaseApiOut[self.schema_create], name=f'{model_name}Create',
                   summary=f'{model_name} Create',
                   dependencies=depends_create)
        async def handle_create(item: schema_create):
            item = self.pre_create(item)
            new_item = await self.model.create_one(item)
            data = await self.schema_create.from_tortoise_orm(new_item)
            return BaseApiOut(data=data)

        @self.post('/create/all', response_model=BaseApiOut, name=f'{model_name}Create',
                   summary=f'{model_name} CreateAll', dependencies=depends_create)
        async def handle_create_all(items: List[schema_create]):
            items = self.pre_create_all(items)
            await self.model.bulk_create([self.model(**item) for item in items], ignore_conflicts=True)
            return BaseApiOut(message='批量创建成功')
            pass

        @self.put("/{item_id}", response_model=BaseApiOut[schema_update], name=f'{model_name}Update',
                  summary=f'{model_name} Update',
                  dependencies=depends_update)
        async def handle_update(item_id: str, item: schema_update):
            item = await self.pre_update(item, item_id=item_id)
            updated_item = await self.model.update_one(item_id, item)
            # data = await schema_update.from_queryset_single(updated_item)
            data = await schema_update.from_queryset(updated_item)
            return BaseApiOut(data=data)

        @self.put('/update/all', response_model=BaseApiOut, name=f'{model_name}Update',
                  summary=f'{model_name} UpdateAll', dependencies=depends_update)
        async def handle_update_all(items: List[schema_update]):
            for item in items:
                await handle_update(item.id, item)
            return BaseApiOut(message='批量更新成功')

        @self.delete("/{item_ids}", description='删除1条或多条数据example：1,2',
                     response_model=BaseApiOut[self.schema_delete], name=f'{model_name}Delete',
                     summary=f'{model_name} Delete',
                     dependencies=depends_delete)
        async def handle_delete(item_ids: str):
            ids = item_ids.split(',')
            data = await self.model.delete_many(ids)
            return BaseApiOut(data=data)

        return self


__all__ = [
    'ModelCrud'
]
