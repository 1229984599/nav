from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class UserList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    nickname: str | None = None
    status: bool
    is_super: bool
    order: int | None = 0
    create_time: datetime | None = None
    update_time: datetime | None = None


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nickname: str | None = None
    status: bool | None = None
    password: str | None = None
    order: int | None = None


class UserFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str | None = None
    status: bool | None = None


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    password: str
    nickname: str | None = None
    status: bool = False
    is_super: bool = False


class UserUpdateAll(UserUpdate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProfileUpdate(BaseModel):
    nickname: str | None = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class RegisterSchema(BaseModel):
    username: str
    password: str
    nickname: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token: str = ""
    refreshToken: str = ""
    expires: datetime
