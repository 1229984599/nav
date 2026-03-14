import traceback
import json

from tortoise.exceptions import IntegrityError

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from fastapi import FastAPI, Request, HTTPException
from loguru import logger
from starlette.responses import JSONResponse
from common.response import BaseApiOut
from settings import settings


def _log_exception_event(event: str, request: Request, exc: Exception) -> None:
    payload = {
        "event": event,
        "method": request.method,
        "url": str(request.url),
        "error_type": exc.__class__.__name__,
        "error": str(exc),
        "traceback": traceback.format_exc(),
    }
    logger.error(json.dumps(payload, ensure_ascii=False, default=str))


def _safe_message(default: str, exc: Exception) -> str:
    """DEBUG 模式返回原始异常信息，生产环境返回通用描述"""
    if settings.DEBUG:
        return str(exc)
    return default


def register_exception(app: FastAPI) -> None:
    """
    全局异常捕获
    """

    # tortoise-orm 数据库约束错误
    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        _log_exception_event("integrity_error", request, exc)
        return JSONResponse(
            content=BaseApiOut[str](code=421, message=_safe_message("数据冲突，请检查输入", exc)).model_dump())

    @app.exception_handler(ValueError)
    async def value_exception_handler(request: Request, exc: ValueError):
        _log_exception_event("value_error", request, exc)
        return JSONResponse(
            content=BaseApiOut[str](code=421, message=_safe_message("参数错误", exc)).model_dump())

    @app.exception_handler(KeyError)
    async def key_exception_handler(request: Request, exc: KeyError):
        _log_exception_event("key_error", request, exc)
        return JSONResponse(
            content=BaseApiOut[str](code=421, message=_safe_message("参数缺失", exc)).model_dump())

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """内部参数验证异常"""
        _log_exception_event("validation_error_internal", request, exc)
        return JSONResponse(
            content=BaseApiOut[str](code=421, message=_safe_message("数据验证失败", exc)).model_dump())

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """请求参数验证异常"""
        _log_exception_event("validation_error_request", request, exc)
        return JSONResponse(
            content=BaseApiOut[str](code=422, message=_safe_message("请求参数校验异常", exc)).model_dump())

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        return JSONResponse(
            content=BaseApiOut[str](code=exc.status_code,
                                    message=exc.detail).model_dump())

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """全局所有异常"""
        _log_exception_event("unhandled_exception", request, exc)
        return JSONResponse(
            content=BaseApiOut[str](code=500, message=_safe_message("服务器内部错误", exc)).model_dump())
