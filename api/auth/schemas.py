from datetime import datetime

from pydantic import BaseModel

from models import User


class UserList(User.schema_list(exclude=('password',))):
    pass


class UserUpdate(User.schema_update(include=('nickname', 'status', 'password'))):
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires: datetime
