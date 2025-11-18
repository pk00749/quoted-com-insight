---
id: TASK-006
type: change
title: Docker Compose 部署 Nginx 与应用
status: done
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-004]
risk_level: low
---
# TASK-006 Docker Compose 部署 Nginx 与应用
状态: ✅ 已完成
范围: docker-compose.yml / nginx.conf
需求摘要:
- Nginx SSL 反代应用容器
实现要点:
- 两服务同网络
- 80 -> 301 跳转 443
- SSL 证书目录挂载占位
验收:
- compose up 正常, Nginx 反代 /health
依赖与风险:
- 证书正确挂载
变更记录:
- 2025-11-17 配置提交
