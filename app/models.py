from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class BaseResponse(BaseModel):
    """统一响应格式"""
    success: bool = True
    data: Optional[Dict] = None
    message: str = "操作成功"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class ErrorResponse(BaseModel):
    """错误响应格式"""
    success: bool = False
    data: Optional[Dict] = None
    message: str = "操作失败"
    error: Dict[str, str]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class Announcement(BaseModel):
    """公告信息"""
    id: str = Field(..., description="公告ID")
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="名称")
    title: str = Field(..., description="公告标题")
    publish_date: str = Field(..., description="公告日期")
    category: str = Field(..., description="公告类型")
    url: Optional[str] = Field(None, description="公告链接")

class AnnouncementList(BaseModel):
    """公告列表"""
    announcements: List[Announcement] = Field(..., description="公告列表")
    total: int = Field(..., description="总数量")
    page: int = Field(default=1, description="页码")
    size: int = Field(default=20, description="每页大小")

class AnnouncementSummary(BaseModel):
    """公告智能总结"""
    model_config = {"protected_namespaces": ()}

    summary: str = Field(..., description="智能总结标题")
    content: str = Field(..., description="智能总结内容（500字以内）")
    word_count: int = Field(..., description="字数统计")
    model_info: Dict[str, str] = Field(..., description="模型信息")

class AnnouncementSummarizeRequest(BaseModel):
    """公告总结请求"""
    stock_code: str = Field(..., description="股票代码")

class WebhookRequest(BaseModel):
    """Webhook请求"""
    stock_codes: List[str] = Field(..., description="股票代码列表")
    date: Optional[str] = Field(None, description="指定日期")
    callback_url: Optional[str] = Field(None, description="回调地址")
