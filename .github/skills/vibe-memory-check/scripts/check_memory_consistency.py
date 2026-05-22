#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vibe-harness memory consistency checker.

Checks consistency among:
- memory-bank/memory-registry.yaml
- docs/LESSONS.md
- docs/LESSONS_ARCHIVE.md
- docs/AI_CHANGELOG.md
- evolution/lesson-index.json

This script intentionally uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path.cwd()

REQUIRED_FILES = [
    "AGENTS.md",
    "memory-bank/memory-registry.yaml",
    "memory-bank/activeContext.md",
    "memory-bank/progress.md",
    "memory-bank/architecture.md",
    "memory-bank/tech-stack.md",
    "docs/LESSONS.md",
    "docs/LESSONS_ARCHIVE.md",
    "docs/LESSONS_RULES.md",
    "docs/AI_CHANGELOG.md",
    "evolution/lesson-index.json",
    "evolution/promotion-log.md",
]

STATUS_ALLOWED = {"活跃", "已归档", "Pinned", "active", "archived", "pinned"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_lessons_index(text: str) -> Dict[str, Dict[str, str]]:
    rows: Dict[str, Dict[str, str]] = {}
    in_index = False
    for line in text.splitlines():
        if line.strip() == "## 索引":
            in_index = True
            continue
        if in_index and line.startswith("## "):
            break
        if not in_index:
            continue
        if not line.startswith("|") or "---" in line or "#" in line and "标题" in line:
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 5:
            continue
        lesson_id, title, tags, priority, status = cols[:5]
        if re.fullmatch(r"L\d+", lesson_id):
            rows[lesson_id] = {"title": title, "tags": tags, "priority": priority, "status": status}
    return rows


def parse_lesson_headings(text: str) -> List[str]:
    return re.findall(r"^##\s+(L\d+)\b", text, flags=re.M)


def normalize_status(status: str) -> str:
    if status in {"Pinned", "pinned"}:
        return "Pinned"
    if status in {"活跃", "active"}:
        return "active"
    if status in {"已归档", "archived"}:
        return "archived"
    return status


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check(strict: bool = False) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            (errors if strict else warnings).append(f"missing required file: {rel}")

    lessons_path = ROOT / "docs/LESSONS.md"
    lessons_text = read(lessons_path)
    if lessons_text:
        index = parse_lessons_index(lessons_text)
        headings = parse_lesson_headings(lessons_text)
        heading_set = set(headings)

        if not index:
            errors.append("docs/LESSONS.md has no parseable index rows")

        duplicate_headings = sorted({x for x in headings if headings.count(x) > 1})
        for lid in duplicate_headings:
            errors.append(f"duplicate lesson heading: {lid}")

        for lid, row in index.items():
            if row["status"] not in STATUS_ALLOWED:
                errors.append(f"lesson {lid} has invalid status: {row['status']}")
            if normalize_status(row["status"]) != "archived" and lid not in heading_set:
                errors.append(f"active/pinned lesson {lid} is in index but missing body heading")

        active_count = sum(1 for r in index.values() if normalize_status(r["status"]) == "active")
        pinned_count = sum(1 for r in index.values() if normalize_status(r["status"]) == "Pinned")
        if active_count > 12:
            errors.append(f"active lessons overflow: {active_count} > 12")
        elif active_count > 10:
            warnings.append(f"active lessons above target window: {active_count} > 10")
        if pinned_count > 5:
            warnings.append(f"too many pinned lessons: {pinned_count} > 5")

    index_path = ROOT / "evolution/lesson-index.json"
    if index_path.exists():
        try:
            data = load_json(index_path)
            lessons = data.get("lessons", []) if isinstance(data, dict) else []
            ids = [item.get("id") for item in lessons if isinstance(item, dict)]
            dupes = sorted({x for x in ids if ids.count(x) > 1 and x})
            for lid in dupes:
                errors.append(f"duplicate lesson id in lesson-index.json: {lid}")
            if lessons_text:
                md_ids = set(parse_lessons_index(lessons_text).keys())
                json_ids = set(x for x in ids if x)
                missing_in_json = sorted(md_ids - json_ids)
                if missing_in_json:
                    warnings.append("lessons in markdown index missing from lesson-index.json: " + ", ".join(missing_in_json))
        except Exception as exc:
            errors.append(f"invalid evolution/lesson-index.json: {exc}")

    registry = ROOT / "memory-bank/memory-registry.yaml"
    if registry.exists():
        text = read(registry)
        for key in ["agent_contract", "lessons", "lesson_index", "memory_consistency"]:
            if key not in text:
                warnings.append(f"memory-registry.yaml missing expected key text: {key}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="treat missing core files as errors")
    parser.add_argument("--json", action="store_true", help="print JSON result")
    args = parser.parse_args()

    errors, warnings = check(strict=args.strict)
    result = {"ok": not errors, "errors": errors, "warnings": warnings}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if errors:
            print("FAIL: memory consistency check failed")
            for e in errors:
                print(f"ERROR: {e}")
        else:
            print("PASS: memory consistency check passed")
        for w in warnings:
            print(f"WARN: {w}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
