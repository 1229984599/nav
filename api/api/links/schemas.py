from typing import List

from pydantic import BaseModel, Field

from models import Links, Menu

MenuRelation = Menu.schema_list(name='Relation', include=('id', 'title'))


class CreateMenuSchema(Links.schema_create('CreateMenu', )):
    menus: list[int] | None = None


class FilterSchemaList(Links.schema_filters(include=('title', 'menus', 'status'))):
    menus: list[int] | None = None


# class UpdateMenuSchema(Links.schema_update('UpdateMenu', )):
#     menus: list[int] | None = None


class LinkSchemaList(Links.schema_list(exclude='menus', )):
    menus: List[MenuRelation] = Field(default=[])
    pass

# class SetMenuSchema(BaseModel):
#     menus: list[int]
#     link_id: int
