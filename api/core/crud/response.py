from typing import Generic, TypeVar, Optional, Union, List, Dict, Any
from pydantic.generics import GenericModel, BaseModel

_T = TypeVar('_T')


class BaseApiOut(GenericModel, Generic[_T], BaseModel):
    message: str = '请求成功'
    data: Optional[_T] = None
    code: int = 200


# class ItemListSchema(GenericModel, Generic[_T], BaseModel):
#     """数据查询返回格式"""
#     items: Optional[List[_T]]  # 数据列表
#     total: int = None  # 数据总量
#     query: Dict[str, Any] = None
#     filter: Dict[str, Any] = None
#
#
# class ListApiOut(BaseApiOut, Generic[_T]):
#     data: Union[Optional[ItemListSchema[_T]], List]
#     # data: ItemListSchema[_T]
#
#
# class ErrorApiOut(BaseApiOut, Generic[_T]):
#     message: str = '请求失败'
#     data: Optional[_T] = None
#     code: int = 201


__all__ = [
    'BaseApiOut',
    # 'ItemListSchema',
    # 'ListApiOut',
    # 'ErrorApiOut',
]
