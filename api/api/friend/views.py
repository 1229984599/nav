from core.crud import ModelCrud, BaseApiOut
from models import Friend
from ..links.utils import get_site_info

friend_router = ModelCrud(Friend,
                          schema_filters=Friend.schema_filters(include=('title',))
                          ).register_crud()


@friend_router.post('/siteinfo')
async def handle_siteinfo(url: str):
    data = await get_site_info(url)
    return BaseApiOut(data=data)
