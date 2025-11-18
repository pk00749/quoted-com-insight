---
description: 脚手架化创建一个新的 OpenSpec 变更并进行严格校验。
---

$ARGUMENTS
<!-- OPENSPEC:START -->
**防护栏**
- 优先采用直接、最小可行的实现；只有在明确需要或被要求时才增加复杂度。
- 将变更范围严格控制在目标结果之内。
- 如需更多 OpenSpec 约定或说明，请参考 `openspec/AGENTS.md`（位于 `openspec/` 目录中——若未看到可运行 `ls openspec` 或 `openspec update`）。
- 识别任何模糊不清的细节，在动手修改文件前先提出必要的澄清问题。

**步骤**
1. 查看 `openspec/project.md`，运行 `openspec list` 与 `openspec list --specs`，并视需要检查相关代码/文档（例如用 `rg`/`ls`），使提案基于当前行为；记录需要澄清的缺口。
2. 选择一个唯一且以动词开头的 `change-id`，在 `openspec/changes/<id>/` 下脚手架 `proposal.md`、`tasks.md`，以及在需要时添加 `design.md`。
3. 将变更映射为具体能力或需求，若涉及多个范围则拆分为若干规范差异（delta），并明确关系与顺序。
4. 当方案跨越多个系统、引入新模式或需要在编写规范前做权衡时，将架构思考记录在 `design.md`。
5. 在 `changes/<id>/specs/<capability>/spec.md` 中起草规范差异（每个能力一个目录），使用 `## ADDED|MODIFIED|REMOVED Requirements`，并确保至少包含一个 `#### Scenario:`；涉及多个能力时交叉引用。
6. 编写 `tasks.md` 为有序的小颗粒可验证事项，能带来可见进度，包含校验（测试、工具），并标注依赖或可并行项。
7. 使用 `openspec validate <id> --strict` 严格校验，修复全部问题后再共享提案。

**参考**
- 当校验失败时，用 `openspec show <id> --json --deltas-only` 或 `openspec show <spec> --type spec` 检视细节。
- 在撰写新需求前，用 `rg -n "Requirement:|Scenario:" openspec/specs` 搜索现有需求。
- 使用 `rg <keyword>`、`ls` 或直接读文件，确保提案与当前实现现实保持一致。
<!-- OPENSPEC:END -->
