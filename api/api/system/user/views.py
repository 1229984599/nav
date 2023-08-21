from tortoise.contrib.pydantic import PydanticModel

from fastapi_tortoise_crud import ModelCrud

from models import User
from auth import auth, schemas


class UserCrud(ModelCrud):

    @classmethod
    async def pre_create(cls, item: PydanticModel) -> dict:
        item = item.model_dump()
        item['password'] = auth.get_password_hash(item['password'])
        return item

    @classmethod
    async def pre_update(cls, item: PydanticModel, item_id: str) -> dict:
        item_data = item.model_dump(exclude_unset=True)
        if item_data.get('password'):
            item_data['password'] = auth.get_password_hash(item_data['password'])
        return item_data


user_router = UserCrud(User,
                       schema_list=schemas.UserList,
                       schema_filters=User.schema_filters(include=('username',)),
                       schema_update=schemas.UserUpdate,
                       schema_read=schemas.UserList,
                       # dependencies=[Depends(check_permission)]
                       ).register_crud()
