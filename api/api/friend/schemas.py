from pydantic import BaseModel, ConfigDict


class FriendListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    href: str
    icon: str | None = None
    desc: str | None = None
    color: str | None = None
    order: int | None = 0
    status: bool


class FriendCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    href: str
    icon: str | None = None
    desc: str | None = None
    color: str | None = None
    order: int | None = 0
    status: bool = True


class FriendFilterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None = None
    status: bool | None = None


class FriendUpdateAllSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str | None = None
    href: str | None = None
    icon: str | None = None
    desc: str | None = None
    color: str | None = None
    order: int | None = None
    status: bool | None = None

