---
name: vibe-git
description: (AUTO-PERSIST) Git discipline gate. Writes plans/commit-plan.md and updates memory-bank status.
metadata:
  short-description: Git workflow auto-persist
  tags: [vibecoding, git, memory-bank, auto-persist]
---

# vibe-git (AUTO-PERSIST)

## Mandatory reading
- Read `docs/00_SYSTEM_CONTRACT.md`
- Follow `docs/60_GIT.workflow.md`
- Read `memory-bank/prd.md`, `memory-bank/activeContext.md`, `memory-bank/progress.md`

## Auto-persist contract (hard)
Write `plans/commit-plan.md`, append `memory-bank/progress.md`, and update `memory-bank/activeContext.md`.
Fallback: output full contents using ```path blocks.

## 示例

### 示例：生成提交计划（建议手动调用）
**输入（用户）**
> /vibe-git  把当前改动拆成原子提交并给出命令

**你应该做**
1. 先生成 `plans/commit-plan.md`（包含每个提交的变更点、命令、检查项、回滚策略）。
2. 再根据用户确认，执行 git 命令。
3. 追加 `memory-bank/progress.md` 记录实际提交哈希/摘要。

## Additional resources
- 规范与模板：`docs/`
- 核心协议：`docs/00_SYSTEM_CONTRACT.md`
