---
description: 归档已部署的 OpenSpec 变更并更新规范。
argument-hint: change-id
---
<!-- OPENSPEC:START -->
**防护栏**
- 优先采用直接、最小可行的实现；仅在明确需要或被要求时增加复杂度。
- 将改动范围严格限定在目标结果内。
- 如需更多 OpenSpec 约定或说明，请参考 `openspec/AGENTS.md`（位于 `openspec/` 目录——若未看到可执行 `ls openspec` 或 `openspec update`）。

**步骤**
1. 确定需要归档的变更 ID：
   - 若本提示已包含具体变更 ID（例如 `<ChangeId>` 部分），去除首尾空白后直接使用。
   - 若对话只模糊提及（如标题或摘要），运行 `openspec list` 展示候选并请用户确认。
   - 否则回顾对话、运行 `openspec list` 并向用户询问；未确认前不要继续。
   - 仍无法唯一确定时，说明当前无法归档。
2. 用 `openspec list`（或 `openspec show <id>`）校验该变更；若不存在、已归档或尚不满足归档条件则停止。
3. 运行 `openspec archive <id> --yes`，让 CLI 无交互地移动变更并应用规范更新（纯工具类工作可加 `--skip-specs`）。
4. 检查输出以确认目标规范已更新且变更进入 `changes/archive/`。
5. 用 `openspec validate --strict` 再次校验，若异常用 `openspec show <id>` 排查。

**参考**
- 归档前先用 `openspec list` 确认变更 ID。
- 用 `openspec list --specs` 查看更新后的规范；交付前解决任何校验问题。
<!-- OPENSPEC:END -->
