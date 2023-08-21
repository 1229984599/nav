# 异步代码
import functools


def ignore_async_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # 调用被装饰的异步函数
            return await func(*args, **kwargs)
        except Exception as e:
            # 忽略异常并打印错误信息
            print(f"{func.__name__} 发生异常: {e}")

    return wrapper
