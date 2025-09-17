from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ..models import BaseResponse, AnnouncementSummarizeRequest, WebhookRequest
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
async def summarize_announcement(request: AnnouncementSummarizeRequest):
    """智能总结公告（百炼大模型qwen3）"""
    try:
        # 调用公告服务的AI总结功能
        summary_data = await announcement_service.summarize_announcement(
            request.announcement.model_dump() if hasattr(request.announcement, 'model_dump') else request.announcement
        )

        return BaseResponse(
            data=summary_data,
            message="AI总结完成（当前为预留接口）"
        )
    except StockAPIException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI总结服务异常: {str(e)}")

@router.post("/webhook/announcements", response_model=BaseResponse)
async def webhook_announcements(request: WebhookRequest):
    """Webhook接口（为n8n优化）"""
    try:
        results = []
        for stock_code in request.stock_codes:
            announcements = await announcement_service.get_announcements(stock_code)
            results.append({
                "stock_code": stock_code,
                "announcements": announcements.model_dump()
            })

        return BaseResponse(
            data=results,
            message=f"Webhook处理成功，共处理{len(request.stock_codes)}只股票"
        )
    except StockAPIException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook处理异常: {str(e)}")
