#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path.cwd()
ctx = ["Vibe Harness v5 is available. Follow AGENTS.md before non-trivial work."]
if (ROOT / "memory-bank/memory-registry.yaml").exists():
    ctx.append("Read memory-bank/memory-registry.yaml as the project memory map.")
if (ROOT / "docs/LESSONS.md").exists():
    ctx.append("Read docs/LESSONS.md Active Summary, Pinned lessons, and recent active lessons before risky work.")
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "\n".join(ctx)
    }
}, ensure_ascii=False))
