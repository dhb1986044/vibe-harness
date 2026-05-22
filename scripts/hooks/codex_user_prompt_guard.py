#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, sys

KEYWORDS = ["修改", "重构", "优化", "生成", "实现", "修复", "部署", "发布", "AGENTS", "memory", "LESSONS", "skill", "hook", "插件", "配置", "代码", "脚本", "测试", "验证"]
try:
    payload = json.load(sys.stdin)
except Exception:
    payload = {}
prompt = str(payload.get("prompt") or payload.get("user_prompt") or payload.get("message") or "")
if any(k.lower() in prompt.lower() for k in KEYWORDS):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "This looks like a non-trivial engineering task. Follow AGENTS.md lifecycle: MEMORY_BOOTSTRAP, PLAN, XCHECK, GUARD, LESSONS, EVOLVE, MEMORY_CHECK before COMPLETE."
        }
    }, ensure_ascii=False))
