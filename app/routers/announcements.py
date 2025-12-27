import logging
from fastapi import APIRouter, HTTPException
from ..models import BaseResponse
from ..services.announcement_service import announcement_service
from ..core.exceptions import StockAPIException

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/announcements/{stock_code}", response_model=BaseResponse)
async def get_stock_announcements(
    stock_code: str
):
    """获取单个股票过去10天的公告列表"""
    try:
        logger.info("请求公告列表", extra={"stock_code": stock_code})
        announcements = await announcement_service.get_announcements(stock_code)
        logger.info(
            "公告列表获取成功",
            extra={"stock_code": stock_code, "count": announcements.total, "days": announcements.size},
        )
        return BaseResponse(data=announcements.model_dump(), message="获取公告成功")
    except StockAPIException as e:
        logger.warning("公告获取失败", extra={"stock_code": stock_code, "error": e.message})
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.exception("公告获取异常", extra={"stock_code": stock_code})
        raise HTTPException(status_code=500, detail=f"内部服务器错误: {str(e)}")

@router.post("/announcements/{stock_code}/sum", response_model=BaseResponse)
async def summarize_announcements_by_code(stock_code: str):
    """AI智能总结公告（正文提取+LLM预留）"""
    try:
        logger.info("请求公告总结", extra={"stock_code": stock_code})
        summary_data = await announcement_service.summarize_announcements(stock_code)
        logger.info("公告总结完成", extra={"stock_code": stock_code, "word_count": summary_data.get("word_count", 0)})
        return BaseResponse(data=summary_data, message="AI总结完成（当前为预留接口）")
    except StockAPIException as e:
        logger.warning("公告总结失败", extra={"stock_code": stock_code, "error": e.message})
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.exception("公告总结异常", extra={"stock_code": stock_code})
        raise HTTPException(status_code=500, detail=f"AI总结服务异常: {str(e)}")
