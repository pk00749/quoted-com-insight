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
from app.core.config import settings  # 新增：引入配置，用于定时任务时间
from app.core.logging_config import configure_logging

# 配置日志（控制台 + 旋转文件，目录不存在时自动创建）
configure_logging(settings.log_level, settings.log_path)
logger = logging.getLogger(__name__)


async def _seconds_until_next_config_time() -> float:
    """计算距离下一个配置的北京时间 HH:MM 的秒数"""
    try:
        tz = ZoneInfo("Asia/Shanghai")
        now = datetime.now(tz)
        hh, mm = [int(x) for x in settings.subscription_refresh_time.split(":")]
        target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)
        return (target - now).total_seconds()
    except Exception as e:
        logger.warning(f"解析 subscription_refresh_time 失败: {e}，回退24小时")
        return 24 * 3600


async def _run_daily_summaries_loop():
    # 首次等待至下一个配置的时间
    try:
        delay = await _seconds_until_next_config_time()
        logger.info(
            "定时任务初始化，首次执行延迟",
            extra={"delay_seconds": round(delay), "target_time": settings.subscription_refresh_time},
        )
        await asyncio.sleep(delay)
    except Exception as e:
        logger.warning(f"计算首次定时延迟失败: {e}")

    while True:
        try:
            logger.info(
                "开始执行定时任务：汇总订阅股票公告",
                extra={"target_time": settings.subscription_refresh_time},
            )
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
            logger.info("定时任务完成", extra={"updated_codes": total_codes})
        except Exception as e:
            logger.exception(f"定时任务运行异常: {e}")
        # 等待到下一个配置时间
        try:
            delay = await _seconds_until_next_config_time()
            logger.info(
                "下次定时任务时间已计算",
                extra={"delay_seconds": round(delay), "target_time": settings.subscription_refresh_time},
            )
            await asyncio.sleep(delay)
        except Exception as e:
            logger.warning(f"计算下次定时延迟失败: {e}，回退为24小时")
            await asyncio.sleep(24 * 3600)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动后台定时任务
    logger.info("应用启动，创建定时任务")
    task = asyncio.create_task(_run_daily_summaries_loop())
    app.state.daily_task = task
    try:
        yield
    finally:
        # 优雅关闭后台任务
        logger.info("应用停止，取消定时任务")
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
