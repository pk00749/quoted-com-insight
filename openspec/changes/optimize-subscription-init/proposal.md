---
id: CHG-011
change-id: optimize-subscription-init
status: proposed
created: 2025-11-18
updated: 2025-11-18
owners: [dev]
rationale: 避免重复初始化已存在数据库文件提升启动速度
impact: subscription_service 初始化流程
migration: 不需要迁移; 未来可加 meta/version 表
rollback: 恢复总是执行建表逻辑
dependencies: [TASK-007]
risk_level: low
---
# Change: 订阅数据库初始化优化

## Why
减少无意义 SQLite 建表检查，提升启动效率。

## What Changes
- 启动检测 subscriptions.db 文件存在则跳过 _init_db
- 预留版本迁移机制说明

## Impact
- specs: subscription
- code: app/services/subscription_service.py

## Risks / Mitigation
| 风险 | 影响 | 缓解 |
|------|------|------|
| 表结构未来变更 | 无迁移导致异常 | 预留 meta/version 机制 |

