from fastapi import FastAPI

from .exception import register_exception
from .listeners import register_init
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
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
    )

    # 初始化
    register_init(app)

    # 注册路由
    register_router(app)

    # 注册中间件
    register_middleware(app)

    # 注册捕获全局异常
    register_exception(app)
    # 如果不想捕捉任何异常，可以将其注释掉。
    # if not settings.DEBUG:
    #     register_exception(app)
    return app
