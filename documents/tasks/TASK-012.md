---
id: TASK-012
type: change
title: 镜像瘦身优化
status: proposed
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-004]
risk_level: medium
---
# TASK-012 镜像瘦身优化
状态: ❌ 待开发
范围: Dockerfile 优化
需求摘要:
- 减少镜像体积 >=30% 不破坏功能
实现要点(规划):
- 多阶段构建 + 仅 chromium
- 合并 RUN, 清理缓存, .dockerignore
- 字体与依赖精简
验收(规划):
- 体积对比记录
- 功能均正常
依赖与风险:
- 过度精简导致功能缺失
变更记录:
- 2025-11-17 规划记录
