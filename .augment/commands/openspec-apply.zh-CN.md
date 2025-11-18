---
description: 实施已获批准的 OpenSpec 变更并保持任务同步。
argument-hint: change-id
---
<!-- OPENSPEC:START -->
**防护栏**
- 优先采用直接、最小可行的实现；仅在明确需要或被要求时增加复杂度。
- 将改动范围严格限定在目标结果内。
- 如需更多 OpenSpec 约定或说明，请参考 `openspec/AGENTS.md`（位于 `openspec/` 目录——若未看到可执行 `ls openspec` 或 `openspec update`）。

**步骤**
将以下步骤作为 TODO 逐项执行：
1. 阅读 `changes/<id>/proposal.md`、`design.md`（如存在）与 `tasks.md`，确认范围与验收准则。
2. 按顺序完成任务，保持修改最小化且聚焦于本变更。
3. 在更新勾选前确认每一项任务确已完成。
4. 完工后统一更新清单，让每一项都为 `- [x]` 并与事实一致。
5. 需要更多上下文时参考 `openspec list` 或 `openspec show <item>`。

**参考**
- 实施时如需从提案中获取更多上下文，用 `openspec show <id> --json --deltas-only`。
<!-- OPENSPEC:END -->
