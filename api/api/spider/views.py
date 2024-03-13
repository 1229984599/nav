from fastapi import APIRouter
from .utils import get_yiyan, HotSpider
from fastapi_tortoise_crud import BaseApiOut

spider_router = APIRouter()

hot_spider = HotSpider()


@spider_router.get("/yiyan", response_model=BaseApiOut)
async def handle_yiyan_spider():
    data = await get_yiyan()
    if not data:
        return BaseApiOut(code=400, message="获取一言失败")
    return BaseApiOut(data=data)


@spider_router.post("/hot", response_model=BaseApiOut)
async def handle_hot_spider(name: str = 'BaiduHot'):
    data = await hot_spider.get_hot_list(name)
    if not data:
        return BaseApiOut(code=400, message=f"{name}获取热榜失败")
    return BaseApiOut(data=data)
