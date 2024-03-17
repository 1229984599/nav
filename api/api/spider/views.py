from fastapi import APIRouter, Depends
from .utils import get_yiyan, HotSpider, WeatherSpider
from fastapi_tortoise_crud import BaseApiOut
from fastapi_cache.decorator import cache

spider_router = APIRouter()

hot_spider = HotSpider()


@spider_router.get("/yiyan", response_model=BaseApiOut)
async def handle_yiyan_spider():
    data = await get_yiyan()
    if not data:
        return BaseApiOut(code=400, message="获取一言失败")
    return BaseApiOut(data=data)


# 每小时更新一次
@spider_router.get("/hot", response_model=BaseApiOut)
# 每60分钟更新一次热榜数据
# @cache(expire=60 * 60)
async def handle_hot_spider(data=Depends(hot_spider.get_hot_list)):
    if not data:
        return BaseApiOut(code=400, message=f"获取热榜失败")
    return BaseApiOut(data=data)


@spider_router.get("/weather", response_model=BaseApiOut)
# 每10分钟更新一次天气数据
@cache(expire=60 * 10)
async def handle_weather_spider(data=Depends(WeatherSpider().get_weather)):
    if not data['weather']:
        return BaseApiOut(code=400, message=f"获取天气数据失败")
    return BaseApiOut(data=data)
