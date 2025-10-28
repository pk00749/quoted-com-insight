from fastapi import APIRouter, HTTPException
from ..models import BaseResponse
from ..services.announcement_service import announcement_service
from ..core.exceptions import StockAPIException

router = APIRouter()

@router.get("/announcements/{stock_code}", response_model=BaseResponse)
async def get_stock_announcements(
    stock_code: str
):
    """获取单个股票过去10天的公告列表"""
    try:
        announcements = await announcement_service.get_announcements(stock_code)
        return BaseResponse(data=announcements.model_dump(), message="获取公告成功")
    except StockAPIException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内部服务器错误: {str(e)}")

@router.post("/announcements/{stock_code}/sum", response_model=BaseResponse)
async def summarize_announcements_by_code(stock_code: str):
    """AI智能总结公告（正文提取+LLM预留）"""
    try:
        summary_data = await announcement_service.summarize_announcements(stock_code)
        return BaseResponse(data=summary_data, message="AI总结完成（当前为预留接口）")
    except StockAPIException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI总结服务异常: {str(e)}")
