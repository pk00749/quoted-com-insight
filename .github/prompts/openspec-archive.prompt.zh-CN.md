---
description: 归档已部署的 OpenSpec 变更并更新规范。
---

$ARGUMENTS
<!-- OPENSPEC:START -->
**防护栏**
- 优先采用直接、最小可行的实现；只有在明确需要或被要求时才增加复杂度。
- 将变更范围严格控制在目标结果之内。
- 如需更多 OpenSpec 约定或说明，请参考 `openspec/AGENTS.md`（位于 `openspec/` 目录中——若未看到可运行 `ls openspec` 或 `openspec update`）。

**步骤**
1. 确认需要归档的变更 ID：
   - 若此提示已包含明确的变更 ID（例如由斜杠命令参数生成的 `<ChangeId>` 块中），去除首尾空白后直接使用该值。
   - 若对话中只是模糊提到某个变更（如标题或摘要），运行 `openspec list` 显示可能的候选项，展示相关候选并确认用户选择的变更。
   - 否则，请回顾对话、运行 `openspec list`，并向用户询问要归档哪个变更；在得到确认前不要继续。
   - 若仍无法确定唯一变更 ID，请停止并告知当前无法归档。
2. 通过 `openspec list`（或 `openspec show <id>`）校验该变更 ID；若不存在、已归档或尚未可归档，则停止操作。
3. 运行 `openspec archive <id> --yes`，让 CLI 在无交互的情况下移动变更并应用规范更新（仅工具类工作时可使用 `--skip-specs`）。
4. 检查命令输出，确认目标规范已更新且变更已位于 `changes/archive/`。
5. 使用 `openspec validate --strict` 进行校验，如有异常可用 `openspec show <id>` 进一步排查。

**参考**
- 归档前用 `openspec list` 确认变更 ID。
- 用 `openspec list --specs` 检查已刷新规范；在交付前修复任何校验问题。
<!-- OPENSPEC:END -->
