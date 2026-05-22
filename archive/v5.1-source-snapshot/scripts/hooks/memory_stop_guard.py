#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, subprocess, sys
from pathlib import Path
ROOT=Path.cwd(); checker=ROOT/'scripts/check_memory_consistency.py'
if not checker.exists(): sys.exit(0)
res=subprocess.run([sys.executable, str(checker), '--strict'], cwd=str(ROOT), text=True, capture_output=True)
if res.returncode==0: sys.exit(0)
print(json.dumps({"decision":"block","reason":"Memory consistency check failed. Fix before stopping.\n"+res.stdout+res.stderr}, ensure_ascii=False))
sys.exit(0)
