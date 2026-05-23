#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

ROOT = Path.cwd()
ctx = ["Vibe Harness v5 is available. Follow AGENTS.md before non-trivial work."]
registry = ROOT / "memory-bank/memory-registry.yaml"
if registry.exists():
    text = registry.read_text(encoding="utf-8", errors="ignore")
    default_profile = "full"
    m = re.search(r"^\s{2}default_profile:\s*([A-Za-z_]+)", text, re.M)
    if m:
        default_profile = m.group(1)
    ctx.append(
        f"Use read_policy.default_profile={default_profile}; "
        "start with the light context unless the task triggers standard/full expansion."
    )
if (ROOT / "docs/LESSONS.md").exists():
    ctx.append(
        "Read docs/LESSONS.md only for risky/governance work, repeated failures, "
        "or lessons/evolution tasks."
    )
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "\n".join(ctx)
    }
}, ensure_ascii=False))
