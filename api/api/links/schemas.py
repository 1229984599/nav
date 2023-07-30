from typing import List

from pydantic import BaseModel, Field

from models import Links, Menu

MenuRelation = Menu.schema_list(name='Relation', include=('id', 'title'))


class CreateMenuSchema(Links.schema_create('CreateMenu', )):
    menus: list[int] | None


class FilterSchemaList(Links.schema_filters(include=('title', 'menus'))):
    menus: list[int] | None


class UpdateMenuSchema(Links.schema_update('UpdateMenu', )):
    menus: list[int] | None


class LinkSchemaList(Links.schema_list()):
    menus: List[MenuRelation] = Field()
    pass


class SetMenuSchema(BaseModel):
    menus: list[int]
    link_id: int
