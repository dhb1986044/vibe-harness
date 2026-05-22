#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re, sys
try: payload=json.load(sys.stdin)
except Exception: payload={}
text=json.dumps(payload, ensure_ascii=False)
patterns=[r'rm\s+-rf\s+/', r'git\s+push\s+--force', r'git\s+reset\s+--hard', r'git\s+clean\s+-fdx']
for pat in patterns:
    if re.search(pat, text):
        print(json.dumps({"decision":"block","reason":f"Dangerous command blocked by vibe harness: {pat}"}, ensure_ascii=False))
        sys.exit(0)
sys.exit(0)
