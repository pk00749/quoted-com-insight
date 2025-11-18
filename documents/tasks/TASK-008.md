---
id: TASK-008
type: change
title: subscribe 命令返回订阅列表
status: done
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-007]
risk_level: low
---
# TASK-008 subscribe 命令返回订阅列表
状态: ✅ 已完成
范围: wechat subscribe 分支
需求摘要:
- 返回当前用户订阅股票集合 (截断 >100)
实现要点:
- 读取 subscriptions 表 stock_code_list
- 排序, 截断提示
验收:
- 无订阅提示正确
- 有订阅显示升序列表
依赖与风险:
- 大量订阅性能
变更记录:
- 2025-11-17 合入
