change-id: modular-wechat-commands-tests
status: proposed
created: 2025-11-18
updated: 2025-11-18
owners: [dev]
rationale: 解耦命令逻辑并实现离线可测试性
impact: wechat 路由文件拆分 + tests 目录用例
migration: 渐进迁移, 保留旧入口暂时兼容
rollback: 合并回单文件 wechat.py
dependencies: [TASK-005,TASK-007]
risk_level: medium
---
# Change: 微信命令模块化与离线单测

## Why
当前 wechat.py 耦合过重且测试需依赖外部服务，需拆分提升可维护与测试速度。解耦命令逻辑并实现离线可测试性

## What Changes
- 拆分命令处理为独立模块 (add/del/subscribe/query)
- 统一 handle(from_user, content) 接口
- 引入离线 mock 用例覆盖主要分支

## Impact
- specs: wechat
- code: app/routers/commands/*.py, tests/

## Risks / Mitigation
| 风险 | 影响 | 缓解 |
|------|------|------|
| 并发访问订阅 | 数据竞争 | 简单锁或单线程保证 |
---
id: CHG-013

