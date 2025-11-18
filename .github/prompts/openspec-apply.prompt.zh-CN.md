---
description: 实施已获批准的 OpenSpec 变更，并保持任务状态同步。
---

$ARGUMENTS
<!-- OPENSPEC:START -->
**防护栏**
- 优先采用直接、最小可行的实现；只有在明确需要或被要求时才增加复杂度。
- 将变更范围严格控制在目标结果之内。
- 如需更多 OpenSpec 约定或说明，请参考 `openspec/AGENTS.md`（位于 `openspec/` 目录中——若未看到可运行 `ls openspec` 或 `openspec update`）。

**步骤**
将以下步骤作为 TODO 逐一追踪并完成：
1. 阅读 `changes/<id>/proposal.md`、`design.md`（如存在）与 `tasks.md`，确认范围与验收标准。
2. 按顺序完成任务，保持最小化、聚焦于本次变更。
3. 在更新任务状态前确认工作已完成——确保 `tasks.md` 中的每项都已完成。
4. 全部完成后更新清单，将每一项标记为 `- [x]`，并确保与事实一致。
5. 需要更多上下文时，参考 `openspec list` 或 `openspec show <item>`。

**参考**
- 实施时若需更多提案上下文，使用 `openspec show <id> --json --deltas-only`。
<!-- OPENSPEC:END -->
