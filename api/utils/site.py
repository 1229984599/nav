import httpx
from bs4 import BeautifulSoup
import asyncio
from urllib.parse import urlparse, urljoin

from .utils import ignore_async_errors


@ignore_async_errors
async def get_site_info(url: str) -> dict:
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    async with httpx.AsyncClient(headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }) as client:
        response = await client.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 获取icon
    icon = soup.find('link', rel='shortcut icon')
    if icon:
        icon_url = icon.get('href')
    else:
        icon = soup.find('link', rel='icon')
        if icon:
            icon_url = icon.get('href')
        else:
            icon_url = '/favicon.ico'
    icon_url = urljoin(url, icon_url)
    # 获取标题
    title = soup.find('title').text
    # 获取描述信息
    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        description = description.get('content')
    else:
        description = ''
    return {
        'title': title.strip(),
        'icon': icon_url,
        'desc': description.strip()
    }


async def main():
    url = 'https://www.baidu.com/'
    result = await get_site_info(url)
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
