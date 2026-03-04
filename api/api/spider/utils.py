import asyncio
import httpx
from fastapi import HTTPException
from models import Site


# from utils.error import ignore_async_errors


# @ignore_async_errors
async def get_yiyan():
    url = "https://v1.hitokoto.cn/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()


class BaseSpider:
    def __init__(self):
        self.session = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }, verify=False

        )


class HotSpider(BaseSpider):

    async def get_hot_list(self, name: str = '百度'):
        """
        通过pearktrue API获取热榜
        :param name: 平台中文名，如 百度、哔哩哔哩、微博 等
        :return:
        """
        try:
            res = await self.session.get(
                'https://api.pearktrue.cn/api/dailyhot/',
                params={'title': name},
                timeout=10,
            )
            data = res.json()
            if data.get('code') == 200 and data.get('data'):
                return {
                    'name': data.get('name', ''),
                    'updateTime': data.get('updateTime', ''),
                    'data': [
                        {
                            'title': item.get('title', ''),
                            'url': item.get('url', ''),
                            'hot': item.get('hot', ''),
                            'desc': item.get('desc', ''),
                            'mobileUrl': item.get('mobileUrl', ''),
                        }
                        for item in data['data']
                    ],
                }
            return None
        except Exception:
            return None


class WeatherSpider(BaseSpider):

    def __init__(self, key: str = ''):
        super().__init__()
        # self.session.base_url = 'https://devapi.qweather.com/v7/'
        self.key = key

    # @ignore_async_errors
    async def get_weather(self, location: str = '106.5518,29.5627'):
        """
        获取天气
        :param location: 经度,纬度坐标
        :return:
        """
        if not self.key:
            site_info = await Site.first()
            if not site_info.weather_key:
                raise HTTPException(status_code=400, detail='请先在站点设置中配置天气key')
            self.key = site_info.weather_key
        city_name = await self._get_city_info(location)
        weather_data = await self._get_weather_data(location)
        future_weather = await self._get_future_weather(location)
        return {
            'city': city_name,
            'weather': weather_data,
            'future_weather': future_weather
        }

    async def _get_future_weather(self, location):
        """
        获取未来7天天气
        :param location:
        :return:
        """
        resp = await self.session.get('https://devapi.qweather.com/v7/weather/7d', params={
            'key': self.key,
            'location': location
        })
        data = resp.json()
        if data['code'] == '200':
            return data['daily']
        return []

    async def _get_city_info(self, location):
        """
        获取城市名称
        :param location: 经度,纬度坐标
        :return:
        """
        resp = await self.session.get('https://geoapi.qweather.com/v2/city/lookup', params={
            'key': self.key,
            'location': location
        })
        data = resp.json()
        if data['code'] == '200':
            location_list = data['location']
            return location_list[0] if len(location_list) > 0 else ''
        return ''

    async def _get_weather_data(self, location):
        """
        获取天气数据
        :param location:
        :return:
        """
        resp = await self.session.get('https://devapi.qweather.com/v7/weather/now', params={
            'key': self.key,
            'location': location
        })
        data = resp.json()
        if data['code'] == '200':
            return data['now']
        return {}


if __name__ == '__main__':
    print(asyncio.run(WeatherSpider().get_weather('106.5518,29.5627')))
