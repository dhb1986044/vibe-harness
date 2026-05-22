---
applyTo: "memory-bank/**,docs/LESSONS*.md,docs/AI_CHANGELOG.md,docs/agents/**,evolution/**,AGENTS.md,.claude/skills/vibe-*/**,.codex/skills/vibe-*/**,.github/skills/vibe-*/**,.github/instructions/**,.github/copilot-instructions.md,scripts/hooks/**,scripts/sync_vibe_skills.py,scripts/check_memory_consistency.py,scripts/evolve_lessons.py"
description: "vibe-harness 治理面被动注入。改动触达治理路径时强制 MEMORY_CHECK / 三向同步 / lesson-index 引用更新。"
---

# 治理面被动注入（Copilot）

当前文件命中 `applyTo` 的治理路径之一。这意味着你正在修改"会改变代理行为本身"的资产。在 COMPLETE 前必须满足：

## 1. MEMORY_CHECK 门禁（强制）

```bash
python scripts/check_memory_consistency.py --strict
```

退出码 ≠ 0 不得 COMPLETE。Copilot 无 Stop hook，必须**主动**调用。

## 2. 三向同步（若改动 `.claude/skills/vibe-*` 治理四件套契约）

```bash
python scripts/sync_vibe_skills.py --write
python scripts/sync_vibe_skills.py --check
```

`.codex/skills/vibe-*` 与 `.github/skills/vibe-*` 必须字节级一致；`docs/` 子目录允许三端分歧。

## 3. lesson-index 引用回填（若新增 / 修改 LESSONS）

```bash
python scripts/check_memory_consistency.py --update-refs
```

确保 `evolution/lesson-index.json` 的 `referenced_in` / `reference_count` / `last_referenced` 与 `docs/LESSONS.md` 实际引用一致。

## 4. 日志前缀语法（若改动 CHANGELOG / promotion-log / progress / LESSONS 等日志类文档）

每条日期 heading 必须形如 `## [YYYY-MM-DD] <kind> | <summary>`，`<kind>` ∈ `{changelog, promote, lint, progress, evolve, ingest, decision}`。详见 [docs/agents/lessons-policy.md](../../docs/agents/lessons-policy.md) 与 [docs/agents/evolution-policy.md](../../docs/agents/evolution-policy.md)。

## 5. memory 边界（再次强调）

仓库事实进 `memory-bank/`；`/memories/repo/` **禁止**用于仓库事实。详见 [AGENTS.md §11](../../AGENTS.md) 与 [.github/copilot-instructions.md](../copilot-instructions.md)。

## 6. 失败回退

任何 linter 失败先回到 EXEC 修复，不得通过修改 linter 或绕过 `--strict` 来"修复"。
