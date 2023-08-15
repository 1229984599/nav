from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.inmemory import InMemoryBackend

from settings import settings
from migrate import init_data


def register_init(app: FastAPI) -> None:
    """
    初始化连接
    :param app:
    :return:
    """

    @app.on_event("startup")
    async def init_connect():
        # 初始化数据
        await init_data()
        # 连接数据库
        register_tortoise(
            app,
            config=settings.DATABASE_CONFIG,
            generate_schemas=True,  # True 表示连接数据库的时候同步创建表
            add_exception_handlers=True,
        )
        # 初始化 apscheduler
        # schedule.init_scheduler()
        # 初始化fastapi-cache2
        # FastAPICache.init(InMemoryBackend(), prefix='fastapi-cache', expire=60)

    @app.on_event('shutdown')
    async def shutdown_connect():
        """
        关闭
        :return:
        """
