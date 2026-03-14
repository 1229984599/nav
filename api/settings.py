from typing import Optional, Dict
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="data/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 开发模式配置（生产环境务必设置 DEBUG=false）
    DEBUG: bool = False
    # 项目文档
    TITLE: str = "FastApi后台管理模板"
    DESCRIPTION: str = "FastAPI 基于 Tortoise-orm 实现的大型项目框架"
    # 文档地址 默认为docs
    DOCS_URL: str = "/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/redoc"

    # token过期时间 分钟（默认1天）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    # refresh token过期时间 分钟（默认30天）
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # 生产环境保管好 SECRET_KEY（无默认值，必须通过环境变量或 .env 配置）
    SECRET_KEY: str = "development key"

    # CORS 允许的来源列表
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:9527"]

    # 项目根路径
    BASE_PATH: Path = Path(__file__).resolve().parent

    # 数据库连接配置
    DATABASE_URI: str = "sqlite://data/data.db"

    # 数据库配置（动态属性，不从 env 读取）
    @property
    def DATABASE_CONFIG(self) -> Dict:
        return {
            'connections': {
                'default': self.DATABASE_URI
            },
            'apps': {
                'models': {
                    'default_connection': 'default',
                    'models': ['models']
                }
            },
            'use_tz': False,
            'timezone': 'Asia/Shanghai'
        }


@lru_cache()
def get_settings():
    return APISettings()


settings = get_settings()
