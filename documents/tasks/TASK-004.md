---
id: TASK-004
type: change
title: Dockerfile 检查与优化
status: done
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: []
risk_level: medium
---
# TASK-004 Dockerfile 检查与优化
状态: ✅ 已完成
范围: 容器构建环境
需求摘要:
- 可运行 FastAPI + Playwright + pdfplumber + AKShare
- 国内源加速, 非 root 运行, 健康检查
实现要点:
- 安装 Chromium (playwright install)
- apt 国内源与缓存清理
- HEALTHCHECK / 非root 用户权限
验收:
- 容器启动正常, /health 200
- 浏览器可用
依赖与风险:
- 国内源稳定性
变更记录:
- 2025-11-17 优化完成
