from fastapi import Body, Query

from fastapi_tortoise_crud import ModelCrud, BaseApiOut

from models import User
from utils.faker import faker

user_router = ModelCrud(User).register_crud()


@user_router.post('/faker')
async def handle_faker_data(number: int = Query(default=10)):
    """
    Generate a number of fake users.
    """
    data = await User.bulk_create([
        User(username=faker.name(),
             password=faker.password(),
             nickname=faker.name(),
             ) for i in range(number)], ignore_conflicts=True)
    return BaseApiOut(data=data)
