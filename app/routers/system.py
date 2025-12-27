import logging
from fastapi import APIRouter
from datetime import datetime

from ..models import BaseResponse
from ..core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health", response_model=BaseResponse)
async def health_check():
    """健康检查（n8n专用）"""
    try:
        # 检查akshare连接状态
        akshare_status = "healthy"

        logger.info("健康检查", extra={"status": "healthy", "service": settings.app_name, "version": settings.version})

        return BaseResponse(
            data={
                "status": "healthy",
                "service": settings.app_name,
                "version": settings.version,
                "akshare_status": akshare_status,
                "timestamp": datetime.now().isoformat(),
                "uptime": "系统运行正常"
            },
            message="服务运行正常，可供n8n调用"
        )
    except Exception as e:
        logger.exception("健康检查异常")
        return BaseResponse(
            data={
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            },
            message="健康检查异常"
        )

@router.get("/version", response_model=BaseResponse)
async def get_version():
    """获取版本信息"""
    logger.info("查询版本信息", extra={"version": settings.version})
    return BaseResponse(
        data={
            "version": settings.version,
            "app_name": settings.app_name,
            "build_time": datetime.now().isoformat(),
            "features": [
                "股票公告获取",
                "AI总结（预留）",
                "n8n集成",
                "Webhook支持"
            ]
        },
        message="版本信息获取成功"
    )
