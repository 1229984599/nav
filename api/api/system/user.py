from tortoise.queryset import QuerySet

from fastapi_tortoise_crud import ModelCrud

from models import User
from .utils import get_password_hash


class UserCrud(ModelCrud):
    @classmethod
    def pre_list(cls, queryset: QuerySet, item: dict) -> QuerySet:
        # queryset = queryset.filter(is_delete=False)
        return super().pre_list(queryset, item)

    @classmethod
    def pre_create(cls, item: dict) -> dict:
        item['password'] = get_password_hash(item['password'])
        return item

    @classmethod
    async def pre_update(cls, item: dict, item_id=None) -> dict:
        if item.get('password'):
            item['password'] = get_password_hash(item['password'])
        return item


user_router = UserCrud(User,
                       schema_filters=User.schema_filters(include=('username',))
                       # dependencies=[Depends(check_permission)]
                       ).register_crud()
