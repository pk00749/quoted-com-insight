---
id: TASK-011
type: change
title: 订阅服务初始化优化
status: proposed
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-007]
risk_level: low
---
# TASK-011 订阅服务初始化优化
状态: ❌ 待开发
范围: subscription_service.py
需求摘要:
- 已存在 subscriptions.db 时跳过初始化建表
实现要点(规划):
- 文件存在性检查
- 预留版本迁移机制 meta/version
验收(规划):
- 已有库启动不重建
- 删除库自动重新初始化
依赖与风险:
- 未来表结构升级策略
变更记录:
- 2025-11-17 文档加入
