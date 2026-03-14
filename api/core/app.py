from fastapi import FastAPI

from .exception import register_exception
from .listeners import lifespan
from .middleware import register_middleware
from .router import register_router
from settings import settings


def create_app() -> FastAPI:
    """
    生成FatAPI对象
    :return:
    """
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL if settings.DEBUG else None,
        redoc_url=settings.REDOC_URL if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # 注册路由
    register_router(app)

    # 注册中间件
    register_middleware(app)

    # 注册捕获全局异常
    register_exception(app)

    return app
