from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ..models import BaseResponse, AnnouncementSummarizeRequest, WebhookRequest
from ..services.announcement_service import announcement_service
from ..core.exceptions import StockAPIException

router = APIRouter()

@router.get("/announcements/{stock_code}", response_model=BaseResponse)
async def get_stock_announcements(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD，默认最近30天"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD，默认今天"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页大小")
):
    """获取股票公告列表"""
    try:
        announcements = await announcement_service.get_announcements(
            stock_code, start_date, end_date, page, size
        )
        return BaseResponse(data=announcements.dict(), message="获取公告成功")
    except StockAPIException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内部服务器错误: {str(e)}")

@router.get("/announcements/latest", response_model=BaseResponse)
async def get_latest_announcements(
    date: Optional[str] = Query(None, description="指定日期 YYYY-MM-DD，默认今天"),
    limit: int = Query(50, ge=1, le=200, description="返回数量限制"),
    category: Optional[str] = Query(None, description="公告类别筛选")
):
    """获取最新公告（所有股票）"""
    try:
        announcements = await announcement_service.get_latest_announcements(date, limit, category)
        return BaseResponse(
            data=[ann.dict() for ann in announcements],
            message=f"获取最新公告成功，共{len(announcements)}条"
        )
    except StockAPIException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内部服务器错误: {str(e)}")

@router.post("/announcements/summarize", response_model=BaseResponse)
async def summarize_announcement(request: AnnouncementSummarizeRequest):
    """智能总结公告（百炼大模型qwen3）"""
    try:
        # 调用公告服务的AI总结功能
        summary_data = await announcement_service.summarize_announcement(
            request.announcement.dict() if hasattr(request.announcement, 'dict') else request.announcement
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
            announcements = await announcement_service.get_announcements(
                stock_code, None, request.date, 1, 50
            )
            results.append({
                "stock_code": stock_code,
                "announcements": announcements.dict()
            })

        return BaseResponse(
            data=results,
            message=f"Webhook处理成功，共处理{len(request.stock_codes)}只股票"
        )
    except StockAPIException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内部服务器错误: {str(e)}")
