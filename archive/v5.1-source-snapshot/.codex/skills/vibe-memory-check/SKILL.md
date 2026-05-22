---
name: vibe-memory-check
description: Check AGENTS, memory-bank, LESSONS, and evolution consistency before COMPLETE.
---

# vibe-memory-check

Use before COMPLETE or after touching AGENTS, memory-bank, docs/LESSONS, docs/AI_CHANGELOG, or evolution files.

Run:

```bash
python scripts/check_memory_consistency.py --strict
```

For legacy onboarding:

```bash
python scripts/check_memory_consistency.py --warn-only
```

Failure means the task must return to REVIEW or EXEC.
