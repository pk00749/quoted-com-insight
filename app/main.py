from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import uvicorn
import logging
import asyncio
from zoneinfo import ZoneInfo
from contextlib import asynccontextmanager

from app.routers import announcements, system
from app.routers import wechat  # 新增：引入微信路由
from app.core.exceptions import create_exception_handler
from app.services.subscription_service import subscription_service
from app.services.announcement_service import announcement_service

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def _seconds_until_next_9am_china() -> float:
    tz = ZoneInfo("Asia/Shanghai")
    now = datetime.now(tz)
    target = now.replace(hour=9, minute=0, second=0, microsecond=0)
    if now >= target:
        target = target + timedelta(days=1)
    return (target - now).total_seconds()


async def _run_daily_summaries_loop():
    # 首次等待至下一个北京时间09:00
    try:
        delay = await _seconds_until_next_9am_china()
        logger.info(f"定时任务将在 {delay:.0f}s 后(北京时间09:00)运行")
        await asyncio.sleep(delay)
    except Exception as e:
        logger.warning(f"计算首次定时延迟失败: {e}")

    while True:
        try:
            logger.info("开始执行09:00定时任务：汇总订阅股票公告")
            rows = subscription_service.all_rows()
            total_codes = 0
            for _, codes in rows:
                for code in codes:
                    try:
                        result = await announcement_service.summarize_announcements(code)
                        subscription_service.save_summary(code, result)
                        total_codes += 1
                    except Exception as ex:
                        logger.error(f"生成 {code} 公告总结失败: {ex}")
            logger.info(f"定时任务完成，更新 {total_codes} 个股票的JSON缓存")
        except Exception as e:
            logger.exception(f"定时任务运行异常: {e}")
        # 等待到下一次09:00
        try:
            delay = await _seconds_until_next_9am_china()
            logger.info(f"下次定时任务将在 {delay:.0f}s 后运行")
            await asyncio.sleep(delay)
        except Exception as e:
            logger.warning(f"计算下次定时延迟失败: {e}，回退为24小时")
            await asyncio.sleep(24 * 3600)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动后台定时任务
    task = asyncio.create_task(_run_daily_summaries_loop())
    app.state.daily_task = task
    try:
        yield
    finally:
        # 优雅关闭后台任务
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


# 创建FastAPI应用（使用 lifespan 管理生命周期）
app = FastAPI(
    title="股票公告信息API服务",
    description="基于akshare的股票公告数据API，为n8n工作流提供股票数据接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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
