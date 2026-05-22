---
name: vibe-discovery
description: Read-only discovery for unmanaged legacy projects without AGENTS or memory. Use before coding in human-created historical projects.
---

# vibe-discovery

Use when the repository has no AGENTS.md, no memory-bank, and no lessons.

Rules:

- Read-only first.
- Do not modify code.
- Do not delete or rename files.
- Do not enable blocking hooks.

Run:

```bash
python scripts/discover_project.py --write
```

Outputs:

- PROJECT_DISCOVERY_REPORT.md
- memory-bank/*.draft.md
- AGENTS.draft.md if needed

After discovery, ask for human confirmation before managed harness.
