from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from tortoise import Tortoise

from migrate import init_data
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_data()
    await Tortoise.init(config=settings.DATABASE_CONFIG, _enable_global_fallback=True)
    await Tortoise.generate_schemas()
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield
    await Tortoise.close_connections()
