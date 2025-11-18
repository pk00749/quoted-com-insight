---
id: TASK-009
type: change
title: 定时任务时间配置化与更新时间展示
status: proposed
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-007]
risk_level: low
---
# TASK-009 定时任务时间配置化与更新时间展示
状态: ❌ 待开发
范围: config.yaml / wechat subscribe 展示
需求摘要:
- subscription_refresh_time 配置化
- subscribe 列表中展示每个股票最近 summary 时间
实现要点(规划):
- 解析 HH:MM, 计算下一触发
- 表 subscription_summaries 时间查询 & 格式化
验收(规划):
- 时间配置生效
- 未刷新显示“尚未刷新”
依赖与风险:
- 时区处理与非法格式回退
变更记录:
- 2025-11-17 文档加入
