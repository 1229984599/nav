from datetime import datetime
from models import User
from pydantic import BaseModel


class UserUpdate(User.schema_update(include=('nickname', 'password'))):
    pass


class UserRead(User.schema_read(exclude=('password',))):
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires: datetime
