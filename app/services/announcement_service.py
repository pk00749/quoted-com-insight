import akshare as ak
import pandas as pd
from typing import List, Optional
from datetime import datetime
import logging
import asyncio

from ..models import Announcement, AnnouncementList
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
            else:
                # 转换日期格式 YYYY-MM-DD -> YYYYMMDD
                if '-' in date:
                    date = date.replace('-', '')

            logger.info(f"获取股票公告: {stock_code}, 日期: {date}")

            # 使用akshare获取公告数据 - 在线程池中执行同步操作
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(None, self._get_stock_notice_data, stock_code, date)

            if df is None or df.empty:
                return []

            return str(df['网址'].tolist())
        except Exception as e:
            logger.error(f"获取公告失败: {stock_code}, 错误: {str(e)}")
            raise StockAPIException(f"获取股票公告失败: {str(e)}", "FETCH_ANNOUNCEMENTS_ERROR")

    def _get_stock_notice_data(self, stock_code: str, date: str) -> pd.DataFrame:
        """获取股票公告数据（同步方法，在线程池中执行）"""
        try:
            logger.info(f"调用 ak.stock_notice_report 获取股票 {stock_code} 在 {date} 的公告")

            # 使用akshare的stock_notice_report接口
            df = ak.stock_notice_report(symbol='财务报告', date=date)

            if not df.empty:
                logger.info(f"成功获取公告数据: {len(df)} 条")
                return df
            else:
                logger.warning(f"未获取到公告数据: {stock_code}, {date}")
                return pd.DataFrame()

        except Exception as e:
            logger.error(f"调用 ak.stock_notice_report 失败: {stock_code}, {date}, 错误: {str(e)}")
            return pd.DataFrame()

    def _parse_date(self, date_str: str) -> str:
        """解析日期格式"""
        try:
            if pd.isna(date_str) or str(date_str).strip() == '':
                return datetime.now().strftime('%Y-%m-%d')

            # 处理多种日期格式
            date_str = str(date_str).strip()
            if len(date_str) == 8 and date_str.isdigit():
                # YYYYMMDD格式
                return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            elif '-' in date_str:
                # 已经是YYYY-MM-DD格式
                return date_str.split(' ')[0]  # 去掉时间部分
            else:
                return datetime.now().strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')

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
