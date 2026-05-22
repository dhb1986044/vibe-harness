---
name: vibe-retrofit
description: Upgrade an existing vibe-managed project to v5.1 without breaking old skills or memory.
---

# vibe-retrofit

Use when the project already has AGENTS.md, memory-bank, LESSONS, or old vibe-* skills.

Process:

1. Inventory existing harness files.
2. Generate or update memory-registry.yaml.
3. Generate or update lesson-index.json.
4. Move vibe-init/vibe-alpha/vibe-omega into `_legacy` adapters.
5. Install v5 core skills.
6. Enable hooks in warn-only first.
7. Move to soft_gate and then managed_harness.
