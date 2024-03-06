import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from loguru import logger

from utils.error import ignore_async_errors


@ignore_async_errors
async def get_site_info(url: str) -> dict:
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    async with httpx.AsyncClient(headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }, verify=False) as client:
        response = await client.get(url)
        response.encoding = 'utf-8'
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
        description = description.get('content') or description.get('value')
    else:
        description = ''
    return {
        'title': title.strip(),
        'icon': icon_url,
        'desc': description.strip()
    }


class CdnImg:
    def __init__(self, token, base_url='https://img.ink/api'):
        self.token = token
        # self.username = username
        # self.password = password
        self.session = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'token': self.token
            },
            base_url=base_url,
            verify=False
        )

    async def login(self, username, password):
        resp = await self.session.post('token', data={
            'email': username,
            'password': password
        })
        resp_data = resp.json()
        if resp_data.get('status'):
            self.token = resp_data['data']['token']
            self.session.headers.update({'token': self.token})
            logger.success('登录成功')
            return
        logger.error('登录失败')
        return

    async def get_img_list(self, page: 1, page_size: 20):
        resp = await self.session.post('images', data={
            'page': page,
            'rows': page_size
        })
        if resp.status_code != 200:
            logger.error('获取图片列表失败')
            return
        data = resp.json()
        if data.get('code') == 200:
            logger.success('上传成功')
            return data.get('data')

    @ignore_async_errors
    async def upload_img(self, file: str | bytes, filename=''):
        if isinstance(file, str):
            return await self._upload_img_by_url(file, filename)
        elif isinstance(file, bytes):
            return await self._upload_img_by_file(file, filename)
        # await self._upload_img_by_file()
        pass

    async def _upload_img_by_url(self, url: str, filename=''):
        filename = filename or url.split('/')[-1]
        img_content = (await self.session.get(url)).content
        return await self._upload_img_by_file(img_content, filename)

    async def _upload_img_by_file(self, file: bytes, filename=''):
        filename = filename or 'icon.png'
        resp = await self.session.post('upload', files={'image': (filename, file)}, data={
            'folder': 'navicon'
        })
        data = resp.json()
        if data.get('code') == 200:
            logger.success('上传成功')
            return data.get('data')
        raise AttributeError('上传图片失败')

    async def delete_img(self, _id: str):
        await self.session.post('delete', data={
            'id': _id
        })


async def main():
    # url = 'https://www.baidu.com/'
    # result = await get_site_info(url)
    # print(result)

    img = CdnImg('9c18712f21048e4b4a3c46c804a7c9bf')
    with open('favicon.png', 'rb') as f:
        print(await img.upload_img(f.read(), 'favicon.png'))


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
