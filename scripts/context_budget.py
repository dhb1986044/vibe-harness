#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estimate vibe-harness bootstrap context size by read profile.

The parser is intentionally small and dependency-free. It only understands the
registry fields owned by read_policy profiles, which keeps the budget check
portable across target repositories.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path.cwd()
REGISTRY_REL = "memory-bank/memory-registry.yaml"
PROFILE_NAMES = ("light", "standard", "full")
DEFAULT_BUDGETS = {
    "light": 12_000,
    "standard": 24_000,
    "full": 70_000,
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def estimate_tokens(byte_count: int) -> int:
    return int(math.ceil(byte_count / 4))


def _strip_comment(value: str) -> str:
    # Slice specs use `path#selector`; treat only whitespace-prefixed ` #` as
    # a YAML comment for this compact parser.
    value = re.split(r"\s+#", value, maxsplit=1)[0]
    return value.strip().strip("'\"")


def _parse_bootstrap_order(text: str) -> List[str]:
    files: List[str] = []
    in_bootstrap = False
    for line in text.splitlines():
        if re.match(r"^\s{2}bootstrap_order:\s*$", line):
            in_bootstrap = True
            continue
        if in_bootstrap and re.match(r"^\s{2}[A-Za-z_][\w-]*:", line):
            break
        if in_bootstrap:
            m = re.match(r"^\s{4}-\s+(.+?)\s*$", line)
            if m:
                files.append(_strip_comment(m.group(1)))
    return files


def parse_registry_profiles(text: str) -> Tuple[str, Dict[str, Dict[str, object]], bool]:
    """Return (default_profile, profiles, has_explicit_profiles)."""
    default_match = re.search(r"^\s{2}default_profile:\s*([A-Za-z_]+)", text, re.M)
    default_profile = default_match.group(1) if default_match else "full"

    profiles: Dict[str, Dict[str, object]] = {}
    has_profiles = bool(re.search(r"^\s{2}profiles:\s*$", text, re.M))
    if not has_profiles:
        bootstrap = _parse_bootstrap_order(text)
        profiles["full"] = {
            "files": bootstrap,
            "slices": [],
            "optional_files": [],
            "budget_bytes": DEFAULT_BUDGETS["full"],
        }
        return default_profile, profiles, False

    lines = text.splitlines()
    current_profile = ""
    current_list = ""
    for line in lines:
        profile_match = re.match(r"^\s{4}([A-Za-z_]+):\s*$", line)
        if profile_match:
            current_profile = profile_match.group(1)
            profiles.setdefault(current_profile, {
                "files": [],
                "slices": [],
                "optional_files": [],
                "budget_bytes": DEFAULT_BUDGETS.get(current_profile, 0),
            })
            current_list = ""
            continue

        if not current_profile:
            continue

        if re.match(r"^\s{2}[A-Za-z_][\w-]*:", line):
            current_profile = ""
            current_list = ""
            continue

        key_match = re.match(r"^\s{6}([A-Za-z_]+):\s*(.*?)\s*$", line)
        if key_match:
            key = key_match.group(1)
            value = _strip_comment(key_match.group(2))
            current_list = key if value == "" else ""
            if key == "budget_bytes" and value:
                try:
                    profiles[current_profile]["budget_bytes"] = int(value.replace("_", ""))
                except ValueError:
                    profiles[current_profile]["budget_bytes"] = 0
            continue

        item_match = re.match(r"^\s{8}-\s+(.+?)\s*$", line)
        if item_match and current_list in {"files", "slices", "optional_files"}:
            item = _strip_comment(item_match.group(1))
            profiles[current_profile].setdefault(current_list, [])
            profile_items = profiles[current_profile][current_list]
            if isinstance(profile_items, list):
                profile_items.append(item)

    return default_profile, profiles, True


def _section(text: str, start: str, stop: str | None = None) -> str:
    start_idx = text.find(start)
    if start_idx < 0:
        return ""
    if not stop:
        return text[start_idx:]
    stop_idx = text.find(stop, start_idx + len(start))
    return text[start_idx:] if stop_idx < 0 else text[start_idx:stop_idx]


def _lesson_body(text: str, lesson_id: str) -> str:
    match = re.search(rf"^##\s+{re.escape(lesson_id)}\b.*$", text, re.M)
    if not match:
        return ""
    next_match = re.search(r"^##\s+L\d+\b", text[match.end():], re.M)
    end = len(text) if not next_match else match.end() + next_match.start()
    return text[match.start():end]


def _lesson_index_rows(index_text: str) -> List[Tuple[str, str]]:
    rows: List[Tuple[str, str]] = []
    for line in index_text.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cols = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cols) >= 7 and re.fullmatch(r"L\d+", cols[0]):
            rows.append((cols[0], cols[-1]))
    return rows


def read_slice(root: Path, slice_spec: str) -> Tuple[str, int]:
    path_text, _, selector = slice_spec.partition("#")
    path = root / path_text
    text = read_text(path)
    if not text:
        return path_text, 0

    if selector == "latest_entry":
        headings = list(re.finditer(r"^##\s+\[20\d{2}-[01]\d-[0-3]\d\].*$", text, re.M))
        if not headings:
            return slice_spec, min(len(text.encode("utf-8")), 0)
        start = headings[0].start()
        end = headings[1].start() if len(headings) > 1 else len(text)
        return slice_spec, len(text[start:end].encode("utf-8"))

    recent_match = re.fullmatch(r"active_summary_pinned_recent(\d+)", selector)
    if recent_match:
        recent_count = int(recent_match.group(1))
        summary = _section(text, "## Active Summary", "## 索引")
        index = _section(text, "## 索引", "## Active Lessons")
        rows = _lesson_index_rows(index)
        pinned = [lid for lid, status in rows if status == "Pinned"]
        active = [lid for lid, status in rows if status == "活跃"]
        selected = pinned + active[-recent_count:]
        compact_index_lines: List[str] = []
        for line in index.splitlines():
            if line.startswith("## 索引") or line.startswith("| #") or "---" in line:
                compact_index_lines.append(line)
                continue
            if any(line.startswith(f"| {lid} ") for lid in selected):
                compact_index_lines.append(line)
        compact_index = "\n".join(compact_index_lines) + "\n"
        bodies = "\n".join(_lesson_body(text, lid) for lid in selected)
        content = summary + compact_index + bodies
        return slice_spec, len(content.encode("utf-8"))

    return slice_spec, len(text.encode("utf-8"))


def profile_report(root: Path, profile: str) -> Dict[str, object]:
    registry_path = root / REGISTRY_REL
    registry_text = read_text(registry_path)
    default_profile, profiles, has_profiles = parse_registry_profiles(registry_text)
    if profile == "default":
        profile = default_profile

    profile_data = profiles.get(profile)
    if not profile_data:
        raise ValueError(f"unknown context profile: {profile}")

    files: List[Dict[str, object]] = []
    total_bytes = 0
    for rel in profile_data.get("files", []):
        if not isinstance(rel, str):
            continue
        size = (root / rel).stat().st_size if (root / rel).exists() else 0
        files.append({"path": rel, "kind": "file", "bytes": size, "exists": (root / rel).exists()})
        total_bytes += size
    for spec in profile_data.get("slices", []):
        if not isinstance(spec, str):
            continue
        label, size = read_slice(root, spec)
        files.append({"path": label, "kind": "slice", "bytes": size, "exists": True})
        total_bytes += size

    budget = int(profile_data.get("budget_bytes") or DEFAULT_BUDGETS.get(profile, 0))
    return {
        "profile": profile,
        "default_profile": default_profile,
        "has_explicit_profiles": has_profiles,
        "budget_bytes": budget,
        "total_bytes": total_bytes,
        "estimated_tokens": estimate_tokens(total_bytes),
        "over_budget": bool(budget and total_bytes > budget),
        "files": files,
        "optional_files": profile_data.get("optional_files", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="default", choices=("default",) + PROFILE_NAMES)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        report = profile_report(ROOT, args.profile)
    except Exception as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"FAIL: {exc}")
        return 1

    report["ok"] = not report["over_budget"]
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if report["ok"] else "FAIL"
        print(
            f"{status}: context profile {report['profile']} "
            f"{report['total_bytes']}/{report['budget_bytes']} bytes "
            f"(~{report['estimated_tokens']} tokens)"
        )
        for item in report["files"]:
            print(f"- {item['kind']}: {item['path']} ({item['bytes']} bytes)")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
