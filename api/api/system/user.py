from fastapi import Depends

from tortoise.contrib.pydantic import PydanticModel
from tortoise.queryset import QuerySet

from core.crud import ModelCrud

from models import User
from core.auth import get_password_hash, get_current_user


class UserCrud(ModelCrud):
    @classmethod
    async def pre_list(cls, queryset: QuerySet, item: dict) -> QuerySet:
        # queryset = queryset.filter(is_delete=False)
        return await super().pre_list(queryset, item)

    @classmethod
    def pre_create(cls, item: PydanticModel) -> dict:
        item = super().pre_create(item)
        item['password'] = get_password_hash(item['password'])
        return item

    @classmethod
    async def pre_update(cls, item: PydanticModel, item_id=None) -> dict:
        item = await super().pre_update(item, item_id)
        if item.get('password'):
            item['password'] = get_password_hash(item['password'])
        return item


user_router = UserCrud(User,
                       schema_list=User.schema_list(exclude=('password',)),
                       schema_filters=User.schema_filters(include=('username',))
                       # dependencies=[Depends(check_permission)]
                       ).register_crud(
    depends_create=[Depends(get_current_user)],
    depends_update=[Depends(get_current_user)],
)
