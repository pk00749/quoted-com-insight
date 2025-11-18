# Project Context

## Purpose
A股公告抓取与智能总结服务：提供公告列表、PDF正文提取、AI摘要，及微信订阅/查询/即时刷新能力，支持配置化与可扩展任务式演进。

## Goals
- 快速稳定获取过去 N 天公告基础数据
- 提供统一的智能公告摘要能力（可替换 LLM）
- 微信命令交互：add / del / subscribe / 查询代码 / refresh(规划)
- 低耦合任务体系 + 自动化 CI/CD + 镜像优化

## Tech Stack
- Python 3.12
- FastAPI (API & WeChat callback)
- AKShare (公告数据源)
- Playwright (动态页面与 PDF 链接解析)
- pdfplumber (PDF正文解析)
- SQLite (订阅与摘要时间戳存储)
- GitHub Actions (CI/CD 构建与部署)

## Architecture Overview
- 接入层: FastAPI 路由 (announcements, wechat, system)
- 服务层: announcement_service, subscription_service
- 支撑层: config (env + YAML), llm 适配层, 定时刷新协程
- 数据层: subscriptions.db + summaries/*.json

## Key Capabilities
- 公告列表查询 (过去 N 天, 配置化)
- 公告内容提取 (PDF 优先 + 网页回退)
- AI摘要聚合 (单公告 + 汇总)
- 微信订阅管理 (add/del/subscribe + 定时刷新)
- 即时刷新命令 refresh (规划中)

## Project Conventions

### Code Style
- PEP8 + Black(建议) 规范（未强制化，可后续加入 pre-commit）
- 清晰函数命名: 动词前缀 summarize_announcements / add_code / del_code
- 模块边界：routers / services / core / specs 分离

### Architecture Patterns
- 服务对象 (announcement_service / subscription_service) 管理核心业务
- 异步协程定时任务 + lifespan 管理后台循环
- 配置集中：settings 读取 env + YAML 覆盖

### Testing Strategy
- pytest + pytest-asyncio
- 离线测试要求：通过 monkeypatch/mock 避免真实网络 (Playwright/AKShare/LLM)
- 计划：命令处理模块化后独立测试 (TASK-013)

### Git Workflow
- main 主干；任务通过变更提案 (OpenSpec change) 后实现
- CI：push main & tag -> 构建镜像 + 部署
- Tag 语义化: vX.Y.Z

## Domain Context
A股公告来源巨潮资讯；股票代码 6 位数字。公告可能以 PDF 提供，需优先解析 PDF；若无则解析网页正文。

## Configuration Keys
- announcement_time_range_days: 拉取公告窗口天数
- pdf_content_max_chars: PDF正文截断长度
- subscription_refresh_time: 定时任务时间 (HH:MM, Asia/Shanghai)
- WECHAT_TOKEN: 微信验签 Token

## Non-Functional Requirements
- 稳定与可恢复：异常日志、去重、失败不中断主循环
- 性能：当前规模小，单线程异步即可；后续可增加并发抓取
- 可维护：任务拆分 -> OpenSpec change proposals -> 归档
- 镜像体积优化 (TASK-012 规划)

## External Dependencies
- 巨潮资讯 (AKShare 接口)
- 微信公众平台服务器 (回调验签)
- DashScope / LLM Provider (可替换)

## Important Constraints
- 受限于 AKShare 接口频率 & Playwright 浏览器体积
- 微信消息长度限制 (约 <2000 字 分段策略预留)

## Future Work
- 命令模块化与离线单测 (TASK-013)
- refresh 即时刷新命令 (TASK-014)
- 镜像瘦身 (TASK-012)
- 配置与命令规范化 specs (API.md / WECHAT.md / CONFIG.md)
