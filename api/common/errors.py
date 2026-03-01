from common.response import BaseApiOut


def not_found(resource: str) -> BaseApiOut[None]:
    return BaseApiOut(code=404, message=f"{resource}不存在")

