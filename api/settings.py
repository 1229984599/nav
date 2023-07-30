import os
from typing import Optional, Dict
from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings


class APISettings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = os.environ.get('DEBUG', True)

    # 项目文档
    TITLE: str = "FastApi后台管理模板"
    DESCRIPTION: str = "FastAPI 基于 Tortoise-orm 实现的大型项目框架"
    # 文档地址 默认为docs
    DOCS_URL: str = "/openapi/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/openapi/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/openapi/redoc"

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    # refresh token过期时间 分钟
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 生成token的加密算法
    ALGORITHM: str = os.environ.get('ALGORITHM', 'ALGORITHM')

    # 生产环境保管好 SECRET_KEY
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'dsklfjsladjflsadj')

    # 项目根路径
    BASE_PATH: Path = Path(__file__).resolve().parent.parent

    # 数据库连接配置
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite://system.db')

    # 数据库配置
    DATABASE_CONFIG: Dict = {
        'connections': {
            'default': DATABASE_URI
        },
        'apps': {
            'models': {
                # 设置key值“default”的数据库连接
                'default_connection': 'default',
                'models': ['models', 'models']
            }
        },
        'use_tz': False,
        'timezone': 'Asia/Shanghai'
    }


@lru_cache()
def get_settings():
    return APISettings()


settings = get_settings()
