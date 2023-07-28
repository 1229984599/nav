from fastapi import APIRouter, FastAPI
from api import api_router

router = APIRouter()
router.include_router(api_router, prefix='/api')


def register_router(app: FastAPI) -> None:
    """
    注册路由
    :param app:
    :return:
    """
    # 项目API
    app.include_router(router)


__all__ = [
    "register_router"
]
