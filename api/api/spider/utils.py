import json

import httpx


async def get_yiyan():
    url = "https://v1.hitokoto.cn/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.text


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
