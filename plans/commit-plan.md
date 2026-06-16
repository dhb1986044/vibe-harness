# Commit Plan

## [2026-06-16] git | slim default vibe skill surface

## 目标
- 将默认 Codex lean skill 面从 14 个收窄到核心 8 个。
- 保留完整 `.codex/skills/vibe-*` 源码与 `--skill-set full` 兼容路径。
- 提交并推送当前 `main` 分支。

## 当前状态
- 分支：`main`，跟踪 `origin/main`。
- 变更类型：治理模板、安装器、文档、memory、lesson 引用索引。
- 范围边界：只提交 `D:/workspace/vibe-harness-v5` 当前工程；不触达外部项目。

## 提交拆分

### Commit 1: `chore: slim default vibe skill surface`
- 安装器：`scripts/install_vibe_harness.py` 的 `LEAN_CODEX_SKILLS` 只保留核心 8 个，`full` 仍复制完整技能库。
- 契约/文档：`AGENTS.md`、`docs/agents/**`、`README_DEPLOYMENT.md` 补充 L0-L3 风险分级、默认核心 skill 路由和 optional / advanced / source-only 说明。
- 治理记录：更新 `docs/AI_CHANGELOG.md`、`docs/LESSONS.md`、`memory-bank/**`、`evolution/lesson-index.json`。

## 提交命令
- `git add AGENTS.md README_DEPLOYMENT.md docs/AI_CHANGELOG.md docs/LESSONS.md docs/agents/hooks-and-commands.md docs/agents/memory-model.md docs/agents/onboarding/EXISTING_VIBE_PROJECT_RETROFIT_MANUAL.md docs/agents/onboarding/LEGACY_SKILLS_MIGRATION.md docs/agents/project-modes.md evolution/lesson-index.json memory-bank/activeContext.md memory-bank/progress.md plans/commit-plan.md scripts/install_vibe_harness.py`
- `git commit -m "chore: slim default vibe skill surface"`
- `git push`

## 检查项
- `python -m py_compile scripts/install_vibe_harness.py scripts/check_memory_consistency.py scripts/context_budget.py`
- `python scripts/install_vibe_harness.py --target .tmp/harness-check-discovery --mode discovery --dry-run`
- `python scripts/install_vibe_harness.py --target .tmp/harness-check-retrofit --mode retrofit --dry-run`
- `python scripts/install_vibe_harness.py --target .tmp/harness-check-bootstrap --mode bootstrap --dry-run`
- `python scripts/context_budget.py --profile light --json`
- `python scripts/context_budget.py --profile standard --json`
- `python scripts/sync_vibe_skills.py --check`
- `python scripts/check_memory_consistency.py --strict`
- `git diff --check`
- 新增行 external-project guard：确认 diff 未把外部项目路径写成实施目标。

## 回滚策略
- 提交前：`git restore --staged .`，再按需 `git restore <file>`。
- 提交后、推送前：`git reset --soft HEAD~1` 保留工作区修改。
- 推送后：优先追加 revert/fix commit；不做强推，除非用户再次明确要求。

## 风险评估
- 风险等级：中。
- 主要风险：安装器默认行为变化会影响后续目标项目的 lean 安装面。
- 缓解：dry-run 覆盖 discovery / retrofit / bootstrap，保留 `--skill-set full` 兼容路径，不删除 skill 源码。
