from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import logging

from app.routers import announcements, system
from app.routers import wechat  # 新增：引入微信路由
from app.core.exceptions import create_exception_handler

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="股票公告信息API服务",
    description="基于akshare的股票公告数据API，为n8n工作流提供股票数据接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加异常处理器
app.add_exception_handler(HTTPException, create_exception_handler)

# 注册路由
app.include_router(announcements.router, prefix="/api/v1", tags=["公告信息"])
app.include_router(system.router, prefix="/api/v1", tags=["系统"])
app.include_router(wechat.router, tags=["微信"])  # 新增：微信回调接口（不加前缀，路径为 /wechat/callback）

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "股票公告信息API服务",
        "docs": "/docs",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
