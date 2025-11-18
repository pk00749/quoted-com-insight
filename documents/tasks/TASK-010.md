---
id: TASK-010
type: change
title: GitHub Actions CI/CD 集成
status: done
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: []
risk_level: medium
---
# TASK-010 GitHub Actions CI/CD 集成
状态: ✅ 已完成
范围: .github/workflows/cicd.yml
需求摘要:
- 构建镜像并推送 TCR
- 远程服务器拉取并重启 compose
实现要点:
- 触发: push main / tag v*
- buildx 多标签: latest / build-日期-SHA / vX.Y.Z
- SSH 部署脚本执行
验收:
- main push 自动更新服务
- tag 生成版本镜像
依赖与风险:
- Secrets 安全, SSH 连通
变更记录:
- 2025-11-17 工作流上线
