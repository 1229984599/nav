from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MenuSchemaList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    icon: str
    order: int
    color: str | None = None
    is_vip: bool
    status: bool
    parent_id: int | None = None
    create_time: datetime | None = None
    update_time: datetime | None = None


class MenuSchemaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None = None
    icon: str | None = None
    order: int | None = None
    color: str | None = None
    is_vip: bool | None = None
    status: bool | None = None
    parent_id: int | str | None = None


class MenuSchemaFilters(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None = None
    status: bool | None = None
    parent_id: int | str | None = None


class MenuUpdateAllSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str | None = None
    icon: str | None = None
    order: int | None = None
    color: str | None = None
    is_vip: bool | None = None
    status: bool | None = None
    parent_id: int | str | None = None
