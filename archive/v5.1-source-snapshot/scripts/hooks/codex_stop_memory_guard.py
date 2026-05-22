#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, subprocess, sys
from pathlib import Path
ROOT=Path.cwd()
checker=ROOT/'scripts/check_memory_consistency.py'
if not checker.exists():
    sys.exit(0)
cmd=[sys.executable, str(checker), '--strict']
res=subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True)
if res.returncode==0:
    sys.exit(0)
reason='Memory consistency check failed. Fix AGENTS/memory-bank/LESSONS/evolution before COMPLETE.\n\nSTDOUT:\n'+res.stdout+'\nSTDERR:\n'+res.stderr
# Codex Stop supports decision:block as continuation prompt; common fields continue:false also supported.
print(json.dumps({"decision":"block","reason":reason}, ensure_ascii=False))
sys.exit(0)
