from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

_T = TypeVar("_T")


class BaseApiOut(BaseModel, Generic[_T]):
    code: int = 200
    message: str = "请求成功"
    data: Optional[_T] = None
