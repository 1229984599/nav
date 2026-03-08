from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SiteSchemaPublic(BaseModel):
    """公开接口返回的站点信息，不包含敏感字段"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    desc: str | None = None
    keywords: str | None = None
    icon: str | None = None
    color: str | None = None
    footer: str | None = None
    yiyan: bool
    weather: bool
    copyright: str | None = None
    status: bool


class SiteSchemaList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    desc: str | None = None
    keywords: str | None = None
    icon: str | None = None
    color: str | None = None
    footer: str | None = None
    yiyan: bool
    weather: bool
    weather_key: str | None = None
    copyright: str | None = None
    cdn_img_token: str | None = None
    status: bool
    create_time: datetime | None = None
    update_time: datetime | None = None


class SiteSchemaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | str | None = None
    title: str | None = None
    desc: str | None = None
    keywords: str | None = None
    icon: str | None = None
    color: str | None = None
    footer: str | None = None
    yiyan: bool | None = None
    weather: bool | None = None
    weather_key: str | None = None
    copyright: str | None = None
    cdn_img_token: str | None = None
    status: bool | None = None
