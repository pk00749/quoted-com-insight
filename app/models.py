from pydantic import BaseModel, Field
from typing import Any, Optional, List, Dict
from datetime import datetime

class BaseResponse(BaseModel):
    """统一响应格式"""
    success: bool = True
    data: Optional[Any] = None
    message: str = "操作成功"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class ErrorResponse(BaseModel):
    """错误响应格式"""
    success: bool = False
    error: Dict[str, str]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class Announcement(BaseModel):
    """公告信息"""
    id: str = Field(..., description="公告唯一标识")
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="股票名称")
    title: str = Field(..., description="公告标题")
    publish_date: str = Field(..., description="公告日期")
    category: str = Field(..., description="公告类型")
    url: Optional[str] = Field(None, description="公告网址")

class AnnouncementList(BaseModel):
    """公告列表"""
    announcements: List[Announcement]
    total: int = Field(..., description="总数")
    page: int = Field(1, description="页码")
    size: int = Field(20, description="每页大小")

class AnnouncementSummary(BaseModel):
    """公告智能总结"""
    summary: str = Field(..., description="智能总结内容（500字以内）")
    key_points: List[str] = Field(..., description="核心要点")
    impact_analysis: Dict[str, str] = Field(..., description="影响分析")
    risk_level: str = Field(..., description="风险等级: high|medium|low")
    recommendation: str = Field(..., description="简要投资建议")

class AnnouncementSummarizeRequest(BaseModel):
    """公告总结请求"""
    announcement: Announcement

class WebhookRequest(BaseModel):
    """Webhook请求"""
    stock_codes: List[str] = Field(..., description="股票代码列表")
    date: Optional[str] = Field(None, description="指定日期")
    callback_url: Optional[str] = Field(None, description="回调地址")
