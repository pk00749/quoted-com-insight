---
id: CHG-014
change-id: add-refresh-command
status: proposed
created: 2025-11-18
updated: 2025-11-18
owners: [dev]
rationale: 提供即时刷新能力与定时产出一致
impact: 新增 wechat refresh 命令及缓存更新逻辑
migration: 无, 新增命令
rollback: 移除命令分支
dependencies: [TASK-007]
risk_level: low
---
# Change: 新增 refresh 即时刷新命令

## Why
用户需要在定时任务外立即获取最新公告总结。

## What Changes
- 增加 refreshXXXXXX 命令解析
- 复用 summarize & save_summary 流程
- 添加简单频控 (同代码60秒)
- 不需要马上返回summarize的结果，只需要返回股票代码刷新和当前时间，如600000已刷新，2025-11-18。

## Impact
- specs: wechat
- code: wechat.py / commands/refresh.py (未来)

## Risks / Mitigation
| 风险 | 影响 | 缓解 |
|------|------|------|
| 高频刷新 | 性能与限流 | 基本频控 + 缓存复用 |

