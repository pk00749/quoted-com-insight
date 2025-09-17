from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_exception_handler(request: Request, exc: HTTPException):
    """统一异常处理器"""
    logger.error(f"API错误: {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": str(exc.detail)
            },
            "timestamp": datetime.now().isoformat()
        }
    )

class StockAPIException(Exception):
    """股票API自定义异常"""
    def __init__(self, message: str, code: str = "STOCK_API_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)
