#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path
ROOT=Path.cwd()
msg=[]
if (ROOT/'AGENTS.md').exists(): msg.append('Read AGENTS.md before work.')
if (ROOT/'memory-bank/memory-registry.yaml').exists(): msg.append('Use memory-bank/memory-registry.yaml as project memory map.')
if (ROOT/'docs/LESSONS.md').exists(): msg.append('Read LESSONS Active Summary/Pinned/recent active lessons for non-trivial work.')
print(json.dumps({"hookSpecificOutput":{"additionalContext":"\n".join(msg)}} , ensure_ascii=False))
