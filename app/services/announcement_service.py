import akshare as ak
import pandas as pd
from typing import List
from datetime import datetime, timedelta
import logging
import asyncio
import httpx
import pdfplumber
from io import BytesIO
from playwright.async_api import async_playwright

from ..models import Announcement, AnnouncementList
from ..core.exceptions import StockAPIException

logger = logging.getLogger(__name__)

class AnnouncementService:
    """公告数据服务"""

    def __init__(self):
        pass  # 不需要持久化存储，每次实时获取

    async def get_announcements(
        self,
        stock_code: str
    ) -> AnnouncementList:
        """获取单个股票过去10天的公告列表"""
        try:
            logger.info(f"获取股票公告: {stock_code}, 时间范围: 过去10天")

            # 使用akshare获取过去10天的公告数据 - 在线程池中执行同步操作
            loop = asyncio.get_event_loop()
            all_announcements = await loop.run_in_executor(None, self._get_10_days_announcements, stock_code)

            if not all_announcements:
                return AnnouncementList(announcements=[], total=0, page=1, size=20)

            # 去重处理（基于URL和标题）
            unique_announcements = self._remove_duplicates(all_announcements)

            logger.info(f"成功获取并去重后公告数据: {len(unique_announcements)} 条")

            return AnnouncementList(
                announcements=unique_announcements,
                total=len(unique_announcements),
                page=1,
                size=len(unique_announcements)
            )

        except Exception as e:
            logger.error(f"获取公告失败: {stock_code}, 错误: {str(e)}")
            raise StockAPIException(f"获取股票公告失败: {str(e)}", "FETCH_ANNOUNCEMENTS_ERROR")

    def _get_10_days_announcements(self, stock_code: str) -> List[Announcement]:
        """获取过去10天的股票公告数据（同步方法，在线程池中执行）"""
        all_announcements = []

        # 获取过去10天的日期
        end_date = datetime.now()
        for i in range(10):
            current_date = end_date - timedelta(days=i)
            date_str = current_date.strftime('%Y%m%d')

            try:
                logger.info(f"获取 {stock_code} 在 {date_str} 的公告")
                df = self._get_stock_notice_data(stock_code, date_str)

                if not df.empty:
                    # 转换DataFrame为Announcement对象列表
                    announcements = self._convert_df_to_announcements(df, stock_code)
                    all_announcements.extend(announcements)
                    logger.info(f"日期 {date_str}: 获取到 {len(announcements)} 条公告")
                else:
                    logger.info(f"日期 {date_str}: 无公告数据")

            except Exception as e:
                logger.error(f"获取 {date_str} 公告失败: {str(e)}")
                continue

        return all_announcements

    @staticmethod
    def _get_stock_notice_data(stock_code: str, date: str) -> pd.DataFrame:
        """获取股票公告数据（同步方法，在线程池中执行）"""
        try:
            # 使用akshare的stock_notice_report接口
            df = ak.stock_notice_report(symbol='全部', date=date)
            df_filtered = df[df['代码'] == stock_code]
            return df_filtered
        except Exception as e:
            logger.error(f"调用 ak.stock_notice_report 失败: {stock_code}, {date}, 错误: {str(e)}")
            return pd.DataFrame()

    def _convert_df_to_announcements(self, df: pd.DataFrame, stock_code: str) -> List[Announcement]:
        """将DataFrame转换为Announcement对象列表"""
        announcements = []

        for _, row in df.iterrows():
            announcement = Announcement(
                id=f"{stock_code}_{row.get('序号', len(announcements))}_{row.get('公告日期', '')}",
                stock_code=stock_code,
                stock_name=row.get('名称', ''),
                title=row.get('公告标题', ''),
                publish_date=self._parse_date(row.get('公告日期')),
                category=row.get('公告类型', '其他'),
                url=row.get('网址', '')
            )
            announcements.append(announcement)

        return announcements

    @staticmethod
    def _remove_duplicates(announcements: List[Announcement]) -> List[Announcement]:
        """去重处理，基于URL和标题"""
        seen = set()
        unique_announcements = []

        for announcement in announcements:
            # 创建唯一标识：URL + 标题
            key = f"{announcement.url}_{announcement.title}"
            if key not in seen:
                seen.add(key)
                unique_announcements.append(announcement)

        return unique_announcements

    @staticmethod
    def _parse_date(date_str) -> str:
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

    @staticmethod
    async def summarize_announcement(announcement_data: dict) -> dict:
        """使用百炼大模型总结公告（预留接口）"""
        try:
            # TODO: 集成百炼大模型qwen3
            # 当前返回结构化的预留响应

            summary = {
                "summary": f"【AI总结功能预留】针对股票：{announcement_data.get('stock_code', '未知股票')}的公告总结",
                "content": "基于该股票过去10天的公告内容深度分析，通过百炼大模型Qwen3分析得出最终投资观点和关键信息汇总。（当前为预留接口，500字内）",
                "word_count": 0,
                "model_info": {
                    "model": "qwen3",
                    "provider": "百炼大模型",
                    "status": "接口预留"
                }
            }

            logger.info(f"AI总结请求（预留）: {announcement_data.get('stock_code', '')}")
            return summary

        except Exception as e:
            logger.error(f"AI总结失败: {str(e)}")
            raise StockAPIException(f"AI总结功能异常: {str(e)}", "SUMMARIZE_ERROR")

    async def summarize_announcements(self, stock_code: str):
        """AI智能总结公告（正文提取+LLM预留）"""
        try:
            # 1. 获取公告列表
            announcement_list = await self.get_announcements(stock_code)
            announcements = announcement_list.announcements
            if not announcements:
                return {
                    "summary": f"股票{stock_code}近10天无公告",
                    "content": "",
                    "word_count": 0,
                    "model_info": {
                        "model": "qwen3",
                        "provider": "百炼大模型",
                        "status": "接口预留"
                    }
                }

            # 2. 依次访问每个公告URL，提取正文内容
            contents = []
            for ann in announcements:
                text = await self._extract_announcement_content(ann.url)
                contents.append(text)
            print(contents)
            # 3. 预留LLM调用接口，单条总结与最终汇总
            # TODO: 调用百炼大模型qwen3对每个text生成一句话总结
            single_summaries = [f"【预留AI摘要】{ann.title}" for ann in announcements]
            # TODO: 再次调用LLM对所有单句摘要进行汇总
            final_content = "\n".join(single_summaries)[:500]

            return {
                "summary": f"【AI总结功能预留】针对股票：{stock_code}的公告总结",
                "content": final_content,
                "word_count": len(final_content),
                "model_info": {
                    "model": "qwen3",
                    "provider": "百炼大模型",
                    "status": "接口预留"
                }
            }
        except Exception as e:
            logger.error(f"AI智能总结失败: {stock_code}, 错误: {str(e)}")
            raise StockAPIException(f"AI智能总结失败: {str(e)}", "SUMMARIZE_ERROR")

    async def _extract_announcement_content(self, url: str) -> str:
        """提取公告正文内容，优先从PDF中获取"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url, timeout=30000)

                # 尝试获取PDF链接
                pdf_link_tag = await page.query_selector('a.pdf-link')
                if pdf_link_tag:
                    pdf_url = await pdf_link_tag.get_attribute('href')
                    if pdf_url and pdf_url.endswith('.pdf'):
                        pdf_url = pdf_url.split('?')[0]  # 移除查询参数
                        logger.info(f"发现PDF链接: {pdf_url}")
                        await browser.close()
                        return self._extract_pdf_content(pdf_url)

                # 如果没有PDF链接，回退到网页正文提取
                content_div = await page.query_selector('#notice_content')
                if content_div:
                    content = await content_div.inner_text()
                    await browser.close()
                    return content.strip()

                logger.warning(f"未找到公告正文内容: {url}")
                await browser.close()
                return ""

        except Exception as e:
            logger.error(f"提取公告内容失败: {url}, 错误: {str(e)}")
            return ""

    @staticmethod
    def _extract_pdf_content(pdf_url: str) -> str:
        """提取PDF文件的正文内容"""
        try:
            # 修复示例链接的处理逻辑，确保支持带有查询参数的PDF链接
            pdf_url = pdf_url.split('?')[0]  # 移除查询参数

            response = httpx.get(pdf_url, timeout=30)
            response.raise_for_status()

            with pdfplumber.open(BytesIO(response.content)) as pdf:
                text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())
                return text.strip()

        except Exception as e:
            logger.error(f"提取PDF内容失败: {pdf_url}, 错误: {str(e)}")
            return ""

# 创建服务实例
announcement_service = AnnouncementService()
