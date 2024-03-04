from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import FastAPI, Response, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination


class RouterCacheControlResetMiddleware(BaseHTTPMiddleware):
    """Disable Response headers Cache-Control (set to 'no-cache').

    The initial reason for this is that the fastapi-cache library sets the max-age param of the header
    equal to the expire parameter that is provided to the caching layer (Redis),
    so the response is also cached on the browser side, which in most cases is unnecessary."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response: Response = await call_next(request)
        response.headers.update({
            "Cache-Control": "no-cache"
        })
        return response


def register_middleware(app: FastAPI) -> None:
    """
    请求响应拦截 hook
    https://fastapi.tiangolo.com/tutorial/middleware/
    :param app:
    :return:
    """
    # 支持跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.add_middleware(RouterCacheControlResetMiddleware)
    # 添加登录验证中间件

    # 添加Pagination
    add_pagination(app)
    pass
