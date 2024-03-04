import httpx
from loguru import logger


class CdnImg:
    def __init__(self, token, base_url='https://img.xwyue.com/api/v1'):
        self.token = token
        # self.username = username
        # self.password = password
        self.session = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'token': self.token
            },
            base_url=base_url)

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
        resp = await self.session.post('images', params={
            'page': page,
            'rows': page_size
        })
        if resp.status_code != 200:
            logger.error('获取图片列表失败')
            return
        data = resp.json()

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
        resp = await self.session.post('upload', files={'image': (filename, file)}, data={
            'folder': 'navicon'
        })
        data = resp.json()
        if data.get('code') == 200:
            logger.success('上传成功')
            return data.get('data')


if __name__ == '__main__':
    import asyncio

    img = CdnImg('9c18712f21048e4b4a3c46c804a7c9bf', 'https://img.ink/api')
    asyncio.run(img.upload_img('http://www.pickfree.cn/favicon.png'))
