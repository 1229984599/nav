from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MenuRelation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    icon: str
    color: str | None = None


class CreateMenuSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None = None
    href: str | None = None
    icon: str | None = None
    is_self: bool | None = None
    is_vip: bool | None = None
    desc: str | None = None
    color: str | None = None
    order: int | None = None
    cdn_img_id: int | None = None
    status: bool | None = None
    menus: list[int] | None = None


class FilterSchemaList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None = None
    href: str | None = None
    status: bool | None = None
    menus: list[int] | None = None


class LinkSchemaList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    href: str
    icon: str | None = None
    is_self: bool
    is_vip: bool
    desc: str | None = None
    color: str | None = None
    order: int | None = 0
    cdn_img_id: int | None = None
    status: bool
    create_time: datetime | None = None
    update_time: datetime | None = None
    menus: list[MenuRelation] = Field(default=[])


class LinkUpdateAllSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str | None = None
    href: str | None = None
    icon: str | None = None
    is_self: bool | None = None
    is_vip: bool | None = None
    desc: str | None = None
    color: str | None = None
    order: int | None = None
    cdn_img_id: int | None = None
    status: bool | None = None
    menus: list[int] | None = None


class LinkImportItem(BaseModel):
    title: str
    href: str = ""
    icon: str | None = None
    desc: str | None = None
    color: str | None = None
    is_self: bool = False
    is_vip: bool = False
    order: int = 0
    cdn_img_id: int | None = None
    status: bool = True
    menus: list[str] = []


class LinkImportRequest(BaseModel):
    items: list[LinkImportItem]
    create_menus: list[str] = []
