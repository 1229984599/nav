from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from redis import asyncio as aioredis
from redis.asyncio.connection import ConnectionPool

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from migrate import init_data
from settings import settings


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
        # pool = ConnectionPool.from_url(url="redis://localhost:6379/0")
        # redis = aioredis.Redis(connection_pool=pool)
        # redis = await aioredis.Redis(host='1.14.61.14', password='yuan090855')
        # FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
        FastAPICache.init(InMemoryBackend(), prefix='fastapi-cache')
        pass

    @app.on_event('shutdown')
    async def shutdown_connect():
        """
        关闭
        :return:
        """
        pass
