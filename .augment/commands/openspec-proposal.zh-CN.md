---
description: 为新的 OpenSpec 变更搭建脚手架并进行严格校验。
argument-hint: feature description or request
---
<!-- OPENSPEC:START -->
**防护栏**
- 优先采用直接、最小可行的实现；仅在明确需要或被要求时增加复杂度。
- 将改动范围严格限定在目标结果内。
- 如需更多 OpenSpec 约定或说明，请参考 `openspec/AGENTS.md`（位于 `openspec/` 目录——若未看到可执行 `ls openspec` 或 `openspec update`）。
- 遇到含糊不清的细节，先提出必要的澄清问题，再修改文件。

**步骤**
1. 查看 `openspec/project.md`，运行 `openspec list` 与 `openspec list --specs`，并检视相关代码或文档（如 `rg`/`ls`），确保提案基于当前行为；记录需澄清的缺口。
2. 选择唯一且以动词开头的 `change-id`，在 `openspec/changes/<id>/` 下创建 `proposal.md`、`tasks.md`，以及必要时的 `design.md`。
3. 将变更拆解为明确的能力或需求；多范围时拆分为多个规范差异并注明关系与顺序。
4. 当方案跨系统、引入新模式或需要权衡时，将架构决策写入 `design.md`。
5. 在 `changes/<id>/specs/<capability>/spec.md` 中撰写规范差异，使用 `## ADDED|MODIFIED|REMOVED Requirements`，并至少包含一个 `#### Scenario:`；涉及多个能力时互相引用。
6. 编写小而可验证的 `tasks.md` 事项列表，包含验证（测试、工具），并标注依赖或可并行工作。
7. 运行 `openspec validate <id> --strict` 严格校验，修复所有问题后再分享提案。

**参考**
- 当校验失败时，用 `openspec show <id> --json --deltas-only` 或 `openspec show <spec> --type spec` 审查细节。
- 在新增需求前，用 `rg -n "Requirement:|Scenario:" openspec/specs` 搜索现有需求。
- 通过 `rg <keyword>`、`ls` 或直接阅读文件，确保提案贴近实际实现。
<!-- OPENSPEC:END -->
