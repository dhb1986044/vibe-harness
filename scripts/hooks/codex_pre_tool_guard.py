#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
import sys

PATTERNS = [
    ("linux root recursive delete", r"\brm\s+-(?=[A-Za-z]*r)(?=[A-Za-z]*f)[A-Za-z]+\s+/(?:\s|$)"),
    ("git force push", r"\bgit\s+push\b[^\r\n]*(?:--force(?:-with-lease)?|-f)\b"),
    ("git reset hard", r"\bgit\s+reset\b[^\r\n]*\s--hard\b"),
    ("git clean fdx", r"\bgit\s+clean\s+-(?=[A-Za-z]*f)(?=[A-Za-z]*d)(?=[A-Za-z]*x)[A-Za-z]+\b"),
    ("powershell recursive force delete", r"\bRemove-Item\b(?=[^\r\n]*(?:-Recurse|-r)\b)(?=[^\r\n]*(?:-Force|-f)\b)[^\r\n]*"),
    ("cmd recursive quiet rmdir", r"\b(?:rmdir|rd)\b(?=[^\r\n]*/s\b)(?=[^\r\n]*/q\b)[^\r\n]*"),
    ("cmd recursive quiet del", r"\bdel\b(?=[^\r\n]*/s\b)(?=[^\r\n]*/q\b)[^\r\n]*"),
]

try:
    payload = json.load(sys.stdin)
except Exception:
    payload = {}
text = json.dumps(payload, ensure_ascii=False)
for name, pat in PATTERNS:
    if re.search(pat, text, flags=re.IGNORECASE):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"Blocked dangerous command pattern: {name}"
            }
        }, ensure_ascii=False))
        raise SystemExit(0)
