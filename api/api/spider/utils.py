import json
import asyncio
import httpx
from utils.error import ignore_async_errors


@ignore_async_errors
async def get_yiyan():
    url = "https://v1.hitokoto.cn/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()


@ignore_async_errors
async def get_baidu_suggestions(query: str = ''):
    url = "https://www.baidu.com/su"
    params = {"wd": query, "cb": ""}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    # 提取JSON部分
    # api_response = response.text.split("(")[1].split(")")[0]
    # # 将JSON转换为对象
    # data = json.loads(api_response.replace("'", '"'))
    # 返回百度搜索结果
    return response.text


@ignore_async_errors
async def get_hot_list(name: str):
    async with httpx.AsyncClient(base_url='https://api.gumengya.com/Api/') as client:
        res = await client.get(name, params={
            'format': 'json',
        })
        data = res.json()
        if data['code'] == 200:
            return data['data']
        else:
            return None


if __name__ == '__main__':
    print(asyncio.run(get_yiyan()))
