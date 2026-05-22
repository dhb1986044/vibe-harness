#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, sys, re
try: payload=json.load(sys.stdin)
except Exception: payload={}
text=json.dumps(payload, ensure_ascii=False)
keywords=['修改','重构','实现','修复','部署','发布','AGENTS','memory','LESSONS','hook','skill','代码','测试','验证']
if any(k.lower() in text.lower() for k in keywords):
    print(json.dumps({"hookSpecificOutput":{"additionalContext":"This looks like a non-trivial engineering task. Follow AGENTS.md lifecycle and do not COMPLETE before XCHECK/GUARD/LESSONS/EVOLVE/MEMORY_CHECK as applicable."}}, ensure_ascii=False))
