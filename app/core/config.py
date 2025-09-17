from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """应用配置"""
    app_name: str = "股票公告信息API服务"
    version: str = "1.0.0"
    debug: bool = False

    # API配置
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # 缓存配置
    cache_expire_hours: int = 1

    # LLM配置（预留）
    llm_api_key: Optional[str] = None
    llm_api_url: str = "https://dashscope.aliyuncs.com/api/v1/"

    # 日志配置
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"  # 忽略额外的环境变量

settings = Settings()
