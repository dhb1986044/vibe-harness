#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v5.6 phase-aware Stop hook for Codex.

Identical policy to scripts/hooks/memory_stop_guard.py:
- discovery_only / shadow_harness : warn-only (never block)
- soft_gate                       : block only when errors mention governance_paths
- managed_harness                 : block on any failure
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
CHECKER = ROOT / "scripts" / "check_memory_consistency.py"
REGISTRY = ROOT / "memory-bank" / "memory-registry.yaml"
WARN_ONLY_PHASES = {"discovery_only", "shadow_harness"}


def read_phase():
    if not CHECKER.exists():
        return None
    r = subprocess.run(
        [sys.executable, str(CHECKER), "--print-phase"],
        cwd=str(ROOT), text=True, capture_output=True,
    )
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return None


def read_governance_paths():
    if not REGISTRY.exists():
        return []
    paths = []
    in_block = False
    for line in REGISTRY.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.rstrip()
        if stripped.startswith("governance_paths:"):
            in_block = True
            continue
        if in_block:
            if stripped.lstrip().startswith("- "):
                paths.append(stripped.split("- ", 1)[1].strip())
            elif stripped and not stripped.startswith(" "):
                break
    return paths


def run_check(strict):
    args = [sys.executable, str(CHECKER), "--strict" if strict else "--warn-only", "--json"]
    return subprocess.run(args, cwd=str(ROOT), text=True, capture_output=True)


def errors_touch_governance(errors, gov_paths):
    if not gov_paths:
        return True
    for e in errors:
        for p in gov_paths:
            if p and p in e:
                return True
    return False


def emit_block(reason):
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))


def main():
    if not CHECKER.exists():
        raise SystemExit(0)
    phase_info = read_phase() or {}
    phase = phase_info.get("harness_phase", "managed_harness")

    if phase in WARN_ONLY_PHASES:
        run_check(strict=False)
        raise SystemExit(0)

    result = run_check(strict=True)
    if result.returncode == 0:
        raise SystemExit(0)

    try:
        data = json.loads(result.stdout)
        errors = data.get("errors", [])
    except Exception:
        errors = [result.stdout + "\n" + result.stderr]

    if phase == "soft_gate":
        gov_paths = read_governance_paths()
        if not errors_touch_governance(errors, gov_paths):
            raise SystemExit(0)
        emit_block("soft_gate: governance-face memory check failed.\n\n" + "\n".join(errors))
        raise SystemExit(0)

    emit_block(
        "managed_harness: memory consistency check failed. "
        "Fix memory-registry / lesson-index / LESSONS / changelog before COMPLETE.\n\n"
        + "\n".join(errors)
    )
    raise SystemExit(0)


if __name__ == "__main__":
    main()
