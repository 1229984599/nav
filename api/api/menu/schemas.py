from pydantic import BaseModel
from models import Menu


# LinkSchemaRelate = Links.schema_list()


class SetLinkSchema(BaseModel):
    links: list[int]
    menu_id: int


class MenuSchemaList(Menu.schema_list(exclude=('parent',))):
    pass


class MenuSchemaUpdate(Menu.schema_update(exclude=('parent_id',))):
    parent_id: int | str | None = None
    pass


class MenuSchemaFilters(Menu.schema_filters(include=('title',))):
    parent_id: int | str | None = None
