from fastapi import Depends

from core.crud import ModelCrud, BaseApiOut
from models import Friend
from ..links.utils import get_site_info
from core.auth import get_current_user

friend_router = ModelCrud(Friend,
                          schema_filters=Friend.schema_filters(include=('title',))
                          ).register_crud(
    depends_create=[Depends(get_current_user)],
    depends_update=[Depends(get_current_user)]
)


@friend_router.post('/siteinfo')
async def handle_siteinfo(url: str):
    data = await get_site_info(url)
    return BaseApiOut(data=data)
