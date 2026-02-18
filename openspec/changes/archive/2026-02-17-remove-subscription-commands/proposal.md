# Change: 移除订阅功能及相关命令

## Why
产品方向调整，移除用户订阅管理功能，保留核心的股票代码查询能力，简化系统复杂度。

## What Changes
- **BREAKING** 移除 `subscribe` 命令（用户查询订阅列表）
- **BREAKING** 移除 `add` 命令（添加股票订阅）
- **BREAKING** 移除 `del` 命令（删除股票订阅）
- **BREAKING** 移除 `refresh` 命令（手动刷新公告总结）
- 移除 `subscription_service.py` 服务
- 移除 `commands/subscribe.py`, `commands/add.py`, `commands/delete.py` 命令处理器
- 简化帮助文本，只保留股票代码查询说明

## Impact
- Affected specs: `specs/wechat/spec.md`
- Affected code:
  - `app/routers/wechat.py` - 移除订阅相关路由和处理逻辑
  - `app/services/subscription_service.py` - 删除服务
  - `app/routers/commands/subscribe.py` - 删除
  - `app/routers/commands/add.py` - 删除
  - `app/routers/commands/delete.py` - 删除
  - `app/routers/commands/__init__.py` - 移除相关导入
