---
id: CHG-012
change-id: optimize-image-size
status: proposed
created: 2025-11-18
updated: 2025-11-18
owners: [dev]
rationale: 降低镜像体积与拉取时间
impact: Dockerfile 构建层, CI/CD pipeline
migration: 重建镜像即可
rollback: 恢复原单阶段构建
dependencies: [TASK-004]
risk_level: medium
---
# Change: 镜像瘦身优化

## Why
镜像过大影响部署与传输效率。

## What Changes
- 多阶段构建 (builder + runtime)
- 仅安装 chromium 浏览器
- 清理 apt/pip 缓存与无用层
- 使用 .dockerignore 排除无关文件

## Impact
- specs: docker
- code: Dockerfile, .dockerignore, CI workflow

## Risks / Mitigation
| 风险 | 影响 | 缓解 |
|------|------|------|
| 依赖缺失 | 功能异常 | 渐进瘦身 + 回归测试 |

