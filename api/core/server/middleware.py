from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination


def register_cors(app: FastAPI) -> None:
    """
    支持跨域
    :param app:
    :return:
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_middleware(app: FastAPI) -> None:
    """
    请求响应拦截 hook
    https://fastapi.tiangolo.com/tutorial/middleware/
    :param app:
    :return:
    """
    register_cors(app)
    # 添加登录验证中间件

    # 添加Pagination
    add_pagination(app)
    pass
