---
id: TASK-001
type: change
title: 获取股票公告列表API
status: done
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: []
risk_level: low
---
# TASK-001 获取股票公告列表API

状态: ✅ 已完成

接口: GET /api/v1/announcements/{stock_code}

需求摘要:
- 过去 N 天(默认10)公告基础信息列表
- 去重、异常处理
- 不抓正文内容

实现要点:
- ak.stock_notice_report 循环日期聚合
- 配置化时间范围 (announcement_time_range_days)

验收:
- 返回字段完整
- 异常安全
