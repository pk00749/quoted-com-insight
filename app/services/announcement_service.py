import akshare as ak
import pandas as pd
from typing import List, Optional
from datetime import datetime
import logging
import asyncio

from ..core.exceptions import StockAPIException

logger = logging.getLogger(__name__)

class AnnouncementService:
    """公告数据服务"""

    def __init__(self):
        pass  # 不需要持久化存储，每次实时获取

    async def get_announcements(
        self,
        stock_code: str,
        date: Optional[str] = None
    ) -> str:
        """获取单个股票当天的公告列表"""
        try:
            # 设置默认日期为当天
            if not date:
                date = datetime.now().strftime('%Y%m%d')
            logger.info(f"获取股票公告: {stock_code}, 日期: {date}")

            # 使用akshare获取公告数据 - 在线程池中执行同步操作
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(None, self._get_stock_notice_data, stock_code, date)
            if df is None or df.empty:
                return "[]"

            return str(df['网址'].tolist())
        except Exception as e:
            logger.error(f"获取公告失败: {stock_code}, 错误: {str(e)}")
            raise StockAPIException(f"获取股票公告失败: {str(e)}", "FETCH_ANNOUNCEMENTS_ERROR")

    @staticmethod
    def _get_stock_notice_data(stock_code: str, date: str) -> pd.DataFrame:
        """获取股票公告数据（同步方法，在线程池中执行）"""
        try:
            logger.info(f"调用 ak.stock_notice_report 获取股票 {stock_code} 在 {date} 的公告")

            # 使用akshare的stock_notice_report接口
            df = ak.stock_notice_report(symbol='财务报告', date=date)
            df_filtered = df[df['代码'] == stock_code]
            if not df_filtered.empty:
                logger.info(f"成功获取公告数据: {len(df)} 条")
                return df_filtered
            else:
                logger.warning(f"未获取到公告数据: {stock_code} 在 {date}")
                return pd.DataFrame()

        except Exception as e:
            logger.error(f"调用 ak.stock_notice_report 失败: {stock_code}, {date}, 错误: {str(e)}")
            return pd.DataFrame()

    async def summarize_announcement(self, announcement_data: dict) -> dict:
        """使用百炼大模型总结公告（预留接口）"""
        try:
            # TODO: 集成百炼大模型qwen3
            # 当前返回结构化的预留响应

            summary = {
                "summary": f"【AI总结功能预留】针对公告：{announcement_data.get('title', '未知公告')}",
                "key_points": [
                    "• 关键要点1（待AI生成）",
                    "• 关键要点2（待AI生成）",
                    "• 关键要点3（待AI生成）"
                ],
                "impact_analysis": {
                    "positive_impact": "正面影响分析（待AI生成）",
                    "negative_impact": "负面影响分析（待AI生成）",
                    "neutral_impact": "中性影响分析（待AI生成）"
                },
                "investment_suggestion": "投资建议（待AI生成，500字内）",
                "word_count": 0,  # 待实际总结时计算
                "model_info": {
                    "model": "qwen3",
                    "provider": "百炼大模型",
                    "status": "接口预留"
                }
            }

            logger.info(f"AI总结请求（预留）: {announcement_data.get('title', '')}")
            return summary

        except Exception as e:
            logger.error(f"AI总结失败: {str(e)}")
            raise StockAPIException(f"AI总结功能异常: {str(e)}", "SUMMARIZE_ERROR")

# 创建服务实例
announcement_service = AnnouncementService()
