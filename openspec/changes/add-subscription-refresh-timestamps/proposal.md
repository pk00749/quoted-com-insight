---
id: CHG-009
change-id: add-subscription-refresh-timestamps
status: proposed
created: 2025-11-18
updated: 2025-11-18
owners: [dev]
rationale: 需要配置化定时刷新与在订阅列表展示每只股票更新时间
impact: 修改 wechat 列表展示逻辑及 config 解析
migration: 无结构迁移，仅新增字段与读取逻辑
rollback: 恢复原固定09:00与不显示时间戳
dependencies: [TASK-007]
risk_level: low
---
# Change: 配置化定时刷新时间并展示订阅更新时间

## Why
提升灵活性与可观测性，支持运营按需调整刷新时间并让用户看到各股票最近更新时间。

## What Changes
- 解析 subscription_refresh_time 配置 (HH:MM, Asia/Shanghai)
- subscribe/list/my 输出每个股票 summary 更新时间
- 新增 timestamp 查询逻辑与格式化函数

## Impact
- specs: wechat, config
- code: app/core/config.py, app/main.py 背景任务, app/routers/wechat.py

## Risks / Mitigation
| 风险 | 影响 | 缓解 |
|------|------|------|
| 非法时间格式 | 定时任务失效 | 正则校验+默认回退09:00 |
| 时区混淆 | 显示时间错误 | 统一 Asia/Shanghai 转换 |

## Open Questions
- 后续是否支持多时间点列表?

