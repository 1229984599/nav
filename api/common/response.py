from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, model_validator

_T = TypeVar("_T")


class BaseApiOut(BaseModel, Generic[_T]):
    code: int = 200
    message: str = "请求成功"
    msg: str = "请求成功"
    data: Optional[_T] = None

    @model_validator(mode="after")
    def sync_msg(self):
        """Keep msg and message in sync for backward compatibility."""
        if self.message != "请求成功" and self.msg == "请求成功":
            self.msg = self.message
        elif self.msg != "请求成功" and self.message == "请求成功":
            self.message = self.msg
        return self

