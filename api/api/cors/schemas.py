from pydantic import BaseModel, ConfigDict


class CorsListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    origin: str
    desc: str | None = ''
    order: int | None = 0
    status: bool
    create_time: str | None = None


class CorsCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    origin: str
    desc: str | None = ''
    order: int | None = 0
    status: bool = True


class CorsFilterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    origin: str | None = None
    status: bool | None = None


class CorsUpdateAllSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    origin: str | None = None
    desc: str | None = None
    order: int | None = None
    status: bool | None = None
