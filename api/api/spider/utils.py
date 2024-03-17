import asyncio
import httpx
from bs4 import BeautifulSoup
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

    async def _get_juejin_hot_list(self):
        """
        获取掘金热门文章
        :return:
        """
        res = await self.session.get('https://api.juejin.cn/content_api/v1/content/article_rank', params={
            'category_id': '1',
            'type': 'hot',
        })
        data = res.json()
        if data['err_no'] == 0:
            return map(lambda item: {
                'hot': item['content_counter']['hot_rank'],
                'title': item['content']['title'],
                'url': f"https://juejin.cn/post/{item['content']['content_id']}",
            }, data['data'])
        else:
            return None

    async def _get_52pojie_hot(self):
        """
        获取吾爱破解热帖
        :return:
        """
        data_list = []
        resp = await self.session.get('https://www.52pojie.cn/forum.php?mod=guide&view=hot')
        soup = BeautifulSoup(resp.text, 'lxml')
        item_list = soup.select('#threadlist table tbody')
        for item in item_list:
            hot_item = item.select_one('.num em')
            title_item = item.select_one('.common .xst')
            data_list.append({
                'hot': hot_item.text if hot_item else '',
                'title': title_item.text if title_item else '',
                'url': f"https://www.52pojie.cn/{title_item.get('href')}" if title_item else '',
            })
        return data_list

    # @ignore_async_errors
    async def get_hot_list(self, name: str):
        if name == 'JueJinHot':
            return await self._get_juejin_hot_list()
        if name == '52PoJieHot':
            return await self._get_52pojie_hot()
        return await self._get_gumeng_hot(name)

    async def _get_gumeng_hot(self, name):
        """
        通过故梦api获取热榜
        :param name: 站点名称：如bilibili
        :return:
        """
        res = await self.session.get(f"https://api.gumengya.com/Api/{name}", params={
            'format': 'json',
        })
        data = res.json()
        if data['code'] == 200:
            return data['data']
        else:
            return None


class WeatherSpider(BaseSpider):

    def __init__(self, key: str = ''):
        super().__init__()
        # self.session.base_url = 'https://devapi.qweather.com/v7/'
        self.key = key

    # @ignore_async_errors
    async def get_weather(self, location):
        """
        获取天气
        :param location: 经度,纬度坐标
        :return:
        """
        if not self.key:
            site_info = await Site.first()
            if not site_info.weather_key:
                raise HTTPException(status_code=400, detail='请先在网站设置中配置天气key')
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
