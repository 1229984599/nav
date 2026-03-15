from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from loguru import logger
from tortoise import Tortoise

from migrate import init_data
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_data()
    await Tortoise.init(config=settings.DATABASE_CONFIG, _enable_global_fallback=True)
    await Tortoise.generate_schemas()
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    # 从数据库加载动态 CORS 配置
    from core.middleware import load_cors_origins
    await load_cors_origins()
    # Warm tree cache at startup so the first request is instant
    try:
        from api.menu.views import warm_tree_cache
        await warm_tree_cache()
        logger.info("Tree cache warmed successfully")
    except Exception as e:
        logger.warning(f"Failed to warm tree cache: {e}")
    yield
    await Tortoise.close_connections()
