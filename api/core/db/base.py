# -*- coding: utf-8 -*-
"""
@author: moxiaoying
@create: 2022/10/16
@description: 基础模型
"""
from tortoise import fields

from typing import Type
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseConfig, Extra


class BaseCrudMixin(Model):
    @classmethod
    async def create_one(cls, item: dict):
        return await cls.create(**item)

    @classmethod
    async def find_by(cls, **kwargs):
        return await cls.filter(**kwargs).all()

    @classmethod
    async def find_one(cls, **kwargs):
        return await cls.filter(**kwargs).first()

    @classmethod
    async def update_one(cls, _id: str, item: dict):
        await cls.filter(id=_id).update(**item)
        return cls.get(id=_id)

    @classmethod
    async def delete_one(cls, _id: str) -> int:
        deleted_count = await cls.filter(id=_id).delete()
        return deleted_count

    @classmethod
    async def delete_many(cls, ids: list) -> int:
        deleted_count = await cls.filter(id__in=ids).delete()
        return deleted_count


class ModelConfig(BaseConfig):
    extra: Extra = Extra.ignore


class BaseSchemaMixin:
    @classmethod
    def base_schema(cls: Type[Model], name, include=(), exclude=(), **kwargs):
        name = f'{cls.__name__}Schema{name}'
        optional = kwargs.pop('optional', ()) or cls._meta.fields
        # print(f'{name}\t{optional}')
        # include = kwargs.get('include', ())
        if include:
            return pydantic_model_creator(cls, name=name, include=include, optional=optional, config_class=ModelConfig,
                                          **kwargs)
        return pydantic_model_creator(cls, name=name, config_class=ModelConfig, optional=optional, exclude=exclude,
                                      **kwargs)

    @classmethod
    def schema_list(cls, name='List', include=(), exclude=(), **kwargs):
        return cls.base_schema(name=name, include=include, exclude=exclude, **kwargs)

    @classmethod
    def schema_create(cls, name='Create', include=(), exclude=(), **kwargs):
        return cls.base_schema(name, include=include, exclude=exclude, exclude_readonly=True, **kwargs)

    @classmethod
    def schema_read(cls, name='Read', include=(), exclude=(), **kwargs):
        return cls.base_schema(name, include=include, exclude=exclude, **kwargs)

    @classmethod
    def schema_update(cls, name='Update', include=(), exclude=(), **kwargs):
        return cls.base_schema(name, include=include, exclude=exclude, exclude_readonly=True,
                               **kwargs)

    @classmethod
    def schema_filters(cls, name='Filters', include=(), exclude=(), **kwargs):
        return cls.base_schema(name, include=include, exclude=exclude, exclude_readonly=True,
                               **kwargs)

    @classmethod
    def schema_delete(cls):
        return int


class TimestampMixin:
    created = fields.DatetimeField(
        null=True, auto_now_add=True, description="创建时间")
    updated = fields.DatetimeField(
        null=True, auto_now=True, description="更新时间")


class AbstractBaseModel(Model):
    id = fields.IntField(pk=True)
    is_delete = fields.IntField(
        null=False, default=0, description="逻辑删除:0=未删除,1=删除")

    class Meta:
        abstract = True


class BaseModel(BaseCrudMixin, BaseSchemaMixin, TimestampMixin, AbstractBaseModel):
    pass

    class PydanticMeta:
        backward_relations = False
        exclude = ('is_delete',)

    class Meta:
        abstract = True
        ordering = ['-updated', '-created']


__all__ = [
    'BaseModel'
]
