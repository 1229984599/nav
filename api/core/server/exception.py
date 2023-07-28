import traceback

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from fastapi import FastAPI, Request, HTTPException
from loguru import logger
from starlette.responses import JSONResponse
from fastapi_tortoise_crud import BaseApiOut


def register_exception(app: FastAPI) -> None:
    """
    全局异常捕获
    注意 别手误多敲一个s
    exception_handler
    exception_handlers
    两者有区别
        如果只捕获一个异常 启动会报错
        @exception_handlers(UserNotFound)
    TypeError: 'dict' object is not callable
    :param app:
    :return:
    """

    @app.exception_handler(ValueError)
    async def value_exception_handler(request: Request, exc: ValueError):
        return JSONResponse(
            content=BaseApiOut[str](code=421, message=str(exc)).dict())

    @app.exception_handler(KeyError)
    async def value_exception_handler(request: Request, exc: KeyError):
        return JSONResponse(
            content=BaseApiOut[str](code=421, message=str(exc)).dict())

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """
        内部参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"内部参数验证错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            content=BaseApiOut[str](code=421, message=str(exc)).dict())

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            content=BaseApiOut[str](code=422,
                                    message=str(exc) or '请求参数校验异常').dict())

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        return JSONResponse(
            content=BaseApiOut[str](code=exc.status_code,
                                    message=exc.detail).dict())

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            content=BaseApiOut[str](code=500, message=str(exc)).dict())
