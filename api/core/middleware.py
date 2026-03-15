from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import FastAPI, Response, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from settings import settings

# 动态 CORS origins 内存缓存
_dynamic_origins: set[str] = set()


class DynamicCORSMiddleware(CORSMiddleware):
    """继承 Starlette CORSMiddleware，覆盖 origin 检查以支持运行时动态更新"""

    def is_allowed_origin(self, origin: str) -> bool:
        if self.allow_all_origins:
            return True
        if self.allow_origin_regex is not None and self.allow_origin_regex.fullmatch(origin):
            return True
        # 静态配置 + 数据库动态配置
        if origin in self.allow_origins:
            return True
        return origin in _dynamic_origins


async def load_cors_origins():
    """从数据库 CorsOrigin 表加载活跃的 CORS origins 到内存缓存"""
    from models import CorsOrigin
    _dynamic_origins.clear()
    try:
        origins = await CorsOrigin.filter(status=True).values_list('origin', flat=True)
        _dynamic_origins.update(origins)
    except Exception:
        pass


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
    # 支持跨域（使用动态 CORS 中间件，支持从数据库加载额外域名）
    app.add_middleware(
        DynamicCORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    # 添加Pagination
    add_pagination(app)