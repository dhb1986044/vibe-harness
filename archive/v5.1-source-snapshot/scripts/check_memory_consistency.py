#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vibe-harness memory consistency checker.

No third-party dependencies. Works in strict, warn-only, and discovery modes.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path.cwd()

REQUIRED_CORE = [
    "AGENTS.md",
    "memory-bank/memory-registry.yaml",
    "docs/LESSONS.md",
    "docs/LESSONS_RULES.md",
    "docs/AI_CHANGELOG.md",
    "evolution/lesson-index.json",
    "evolution/promotion-log.md",
]

LESSON_ROW_RE = re.compile(r"\|\s*(L\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
BODY_RE = re.compile(r"^##\s+(L\d+)\s+", re.M)


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def parse_registry_mode() -> tuple[str, str]:
    p = ROOT / "memory-bank/memory-registry.yaml"
    if not p.exists():
        return "unmanaged_legacy", "discovery_only"
    text = p.read_text(encoding="utf-8")
    mode = re.search(r"^project_mode:\s*([^#\n]+)", text, re.M)
    phase = re.search(r"^harness_phase:\s*([^#\n]+)", text, re.M)
    return (mode.group(1).strip() if mode else "unmanaged_legacy", phase.group(1).strip() if phase else "discovery_only")


def parse_lessons():
    p = ROOT / "docs/LESSONS.md"
    if not p.exists():
        return [], []
    text = p.read_text(encoding="utf-8")
    rows = []
    for m in LESSON_ROW_RE.finditer(text):
        lid, title, tags, prio, status = [x.strip() for x in m.groups()]
        if lid == "#":
            continue
        rows.append({"id": lid, "title": title, "tags": tags, "priority": prio, "status": status})
    bodies = BODY_RE.findall(text)
    return rows, bodies


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--warn-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    errors, warnings = [], []
    project_mode, harness_phase = parse_registry_mode()

    for rel in REQUIRED_CORE:
        if not (ROOT / rel).exists():
            msg = f"missing required file: {rel}"
            if harness_phase in {"managed_harness", "soft_gate"} or args.strict:
                errors.append(msg)
            else:
                warnings.append(msg)

    rows, bodies = parse_lessons()
    if rows:
        ids = [r["id"] for r in rows]
        dups = sorted({i for i in ids if ids.count(i) > 1})
        if dups:
            errors.append(f"duplicate lesson ids in index: {dups}")
        active = [r for r in rows if r["status"] == "活跃"]
        pinned = [r for r in rows if r["status"] == "Pinned"]
        if len(active) > 12:
            warnings.append(f"active lessons exceed soft limit 12: {len(active)}")
        if len(pinned) > 8:
            warnings.append(f"too many pinned lessons: {len(pinned)}")
        body_ids = set(bodies)
        missing_body = [r["id"] for r in rows if r["status"] != "已归档" and r["id"] not in body_ids]
        if missing_body:
            warnings.append(f"active/pinned lessons missing body section: {missing_body}")

    idx_path = ROOT / "evolution/lesson-index.json"
    if idx_path.exists():
        try:
            data = json.loads(idx_path.read_text(encoding="utf-8"))
            if "lessons" not in data:
                warnings.append("lesson-index.json has no 'lessons' field")
        except Exception as e:
            errors.append(f"invalid lesson-index.json: {e}")

    result = {"project_mode": project_mode, "harness_phase": harness_phase, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for w in warnings:
            print(f"WARN: {w}")
        for e in errors:
            print(f"ERROR: {e}")
        if errors:
            print("FAIL: memory consistency check failed")
        else:
            print("PASS: memory consistency check passed")

    if args.warn_only:
        return 0
    if args.strict or harness_phase == "managed_harness":
        return 1 if errors else 0
    if harness_phase == "soft_gate":
        return 1 if errors else 0
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
