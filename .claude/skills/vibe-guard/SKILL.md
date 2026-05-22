---
name: vibe-guard
description: Evaluate risk, rollback, assumptions, and residual risk before high-impact changes.
---

# vibe-guard

Use this skill before or during risky changes:

- Core logic rewrite
- Large deletion or refactor
- Schema/API change
- Dependency or build chain change
- Security/token/network change
- Plugin release/manifest/marketplace change

## Required output

```text
Risk level: low / medium / high
Rollback plan:
Key assumptions:
Residual risks:
Required XCHECK:
```

If risk is high and rollback is unclear, reduce scope or stop.
