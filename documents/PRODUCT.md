# PRODUCT

## 概述
本服务提供 A 股公告抓取、PDF内容提取、AI摘要、以及基于微信指令的订阅与查询功能，核心以 FastAPI + AKShare + Playwright + pdfplumber 构建，支持任务化扩展与配置化参数。

## 目标
- 快速获取过去 N 天公告基础数据与智能总结
- 稳定的微信接口：即时查询、订阅、定时刷新、手动刷新（规划中）
- 可配置的时间范围与截断长度
- 通过任务文件进行演进管理，支持后续 CI/CD 与镜像优化

## 核心能力
1. 公告列表查询 (API)
2. 公告内容抓取（网页 + PDF 优先）
3. AI 摘要（可插拔）
4. 订阅管理（SQLite）+ 定时汇总
5. 微信命令：add / del / subscribe / 查询代码（refresh 规划）

## 架构概览
- 接入层：FastAPI 路由 (announcements / wechat)
- 服务层：announcement_service / subscription_service
- 支撑层：config (YAML + 环境变量)、LLM 适配、Playwright 渲染
- 数据存储：SQLite (subscriptions.db) + JSON 缓存 (summaries)

## 配置项
- announcement_time_range_days: 公告时间窗口
- pdf_content_max_chars: PDF正文截断长度
- subscription_refresh_time: 定时刷新时间 (HH:MM)
- WECHAT_TOKEN: 微信验签 token (环境变量)

## 非功能需求
- 稳定：异常日志与去重处理
- 可维护：任务拆分与文档标识
- 镜像优化：多阶段与依赖精简（规划）

## 任务与演进
详见 documents/TASKS.md 索引及 tasks 子目录（规划中拆分成独立 TASK-xxx 文件）。

## OpenAPI 规范生成
运行 documents/generate_docs.py 自动输出 API_SPEC.json（用于后续集成 openspec 或其他 spec 工具）。

## 后续规划
- 命令模块化（任务13）
- refresh 命令（任务14 规划）
- CI/CD 优化与镜像瘦身
- 文档自动化与规格工具集成

