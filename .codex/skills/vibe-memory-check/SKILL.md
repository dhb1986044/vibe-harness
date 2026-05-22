---
name: vibe-memory-check
description: Run memory consistency validation before completing tasks that touch AGENTS.md, memory-bank, LESSONS, evolution, vibe skills, hooks, or changelog.
---

# vibe-memory-check

Use this skill before COMPLETE when any of these paths changed:

- `AGENTS.md`
- `memory-bank/**`
- `docs/LESSONS.md`
- `docs/LESSONS_ARCHIVE.md`
- `docs/LESSONS_RULES.md`
- `docs/AI_CHANGELOG.md`
- `evolution/**`
- `.codex/skills/vibe-*/**`
- `.claude/skills/vibe-*/**`
- `scripts/hooks/**`

## Workflow

1. Run:

```bash
python scripts/check_memory_consistency.py --strict
```

2. If it fails, do not mark COMPLETE.
3. Fix the reported inconsistency.
4. Re-run the command until it passes.

## Common fixes

- Active lessons exceed limit: archive or promote older lessons.
- Index/body mismatch: add missing body or correct status.
- Missing lesson-index item: run `python scripts/evolve_lessons.py --write`.
- Missing registry file: create `memory-bank/memory-registry.yaml`.
