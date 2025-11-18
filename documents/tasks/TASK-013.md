---
id: TASK-013
type: change
title: 微信命令模块化与单元测试
status: proposed
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-005,TASK-007]
risk_level: medium
---
# TASK-013 微信命令模块化与单元测试
状态: ❌ 待开发
范围: wechat 命令拆分 + tests
需求摘要:
- 每个命令独立 py 文件
- 离线单元测试模拟输入输出
实现要点(规划):
- commands 目录: wechat_add/del/subscribe/query
- handle(from_user, content) 统一接口
- pytest + monkeypatch 离线
验收(规划):
- 命令逻辑解耦
- add/del/subscribe/query 用例覆盖主要分支
- 离线无网络通过
依赖与风险:
- 并发访问数据锁设计
变更记录:
- 2025-11-17 文档加入
