from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path
import yaml


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

    # 公告时间范围（天）与PDF正文截断长度（字）
    announcement_time_range_days: int = 10
    pdf_content_max_chars: int = 500

    # 日志配置
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"  # 忽略额外的环境变量


def _load_yaml_config() -> dict:
    """从与本文件同目录的 config.yaml 读取配置（若存在）。"""
    try:
        cfg_path = Path(__file__).parent / "config.yaml"
        if not cfg_path.exists() or yaml is None:
            return {}
        with cfg_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            if not isinstance(data, dict):
                return {}
            return data
    except Exception as ex:
        print(ex)
        return {}


# 先加载环境变量配置
settings = Settings()

# 再读取YAML，并在未显式设置对应环境变量时应用YAML值
_yaml = _load_yaml_config()
if _yaml:
    # 环境变量名称按字段名大写处理
    if "announcement_time_range_days" in _yaml and not os.getenv("ANNOUNCEMENT_TIME_RANGE_DAYS"):
        settings.announcement_time_range_days = int(_yaml.get("announcement_time_range_days", settings.announcement_time_range_days))
    if "pdf_content_max_chars" in _yaml and not os.getenv("PDF_CONTENT_MAX_CHARS"):
        settings.pdf_content_max_chars = int(_yaml.get("pdf_content_max_chars", settings.pdf_content_max_chars))
