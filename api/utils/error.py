# 异步代码
import functools
import json

from loguru import logger


def ignore_async_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # 调用被装饰的异步函数
            return await func(*args, **kwargs)
        except Exception as e:
            payload = {
                "event": "ignore_async_errors",
                "function": func.__name__,
                "error": str(e),
            }
            logger.error(json.dumps(payload, ensure_ascii=False, default=str))

    return wrapper
