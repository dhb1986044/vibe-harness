---
name: vibe-evolve
description: Promote recurring lessons into Guard, XCheck, Skill, Template, or Plugin candidates while preventing skill bloat.
---

# vibe-evolve

Use this skill after LESSONS when a task produced a new failure pattern, repeated error, workflow improvement, or reusable rule.

## Workflow

1. Read `docs/LESSONS.md` Active Summary and index.
2. Determine whether any lesson is repeated, severe, reusable, or automatable.
3. Run:

```bash
python scripts/evolve_lessons.py --write
```

4. Review `evolution/candidates/`.
5. Move accepted candidates into `vibe-guard`, `vibe-xcheck`, or a dedicated skill.
6. Record the decision in `evolution/promotion-log.md`.

## Anti-bloat rule

Do not create a new skill for a single low-risk lesson. Prefer merging into existing guard/xcheck/skill unless the workflow is stable and reusable.
