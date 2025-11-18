---
id: TASK-007
type: change
title: 微信订阅与定时刷新
status: done
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-005]
risk_level: medium
---
# TASK-007 微信订阅与定时刷新
状态: ✅ 已完成
范围: subscription_service / 定时任务 / wechat
需求摘要:
- add/del 维护订阅列表
- 每日固定时间批量生成 JSON 总结
- 查询时返回缓存内容
实现要点:
- SQLite 表 subscriptions + summaries
- 定时协程循环触发
- JSON 文件缓存内容读取
验收:
- add/del 生效
- 定时生成文件
- 代码查询返回内容
依赖与风险:
- 定时任务失败重试
变更记录:
- 2025-11-17 功能完成
