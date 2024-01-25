from fastapi import APIRouter
from .utils import get_yiyan, get_baidu_suggestions
from fastapi_tortoise_crud import BaseApiOut

spider_router = APIRouter()


@spider_router.get("/baidu", response_model=BaseApiOut)
async def baidu_spider(query: str = ''):
    data = await get_baidu_suggestions(query)
    return BaseApiOut(data=data)


@spider_router.get("/yiyan", response_model=BaseApiOut)
async def yiyan_spider():
    data = await get_yiyan()
    print(data)
    return BaseApiOut(data=data)
