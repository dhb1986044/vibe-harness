#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only discovery for unmanaged legacy projects.

Outputs draft files for human review. Never modifies business code.
"""
from __future__ import annotations
import json
import re
import argparse
from pathlib import Path

COMMAND_FILES = [
    "package.json",
    "pyproject.toml",
    "Makefile",
    "README.md",
    "requirements.txt",
    "pom.xml",
    "build.gradle",
    "docker-compose.yml",
    "Dockerfile",
]

EXCLUDE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".pytest_cache"}


def discover(root: Path) -> dict:
    files = []
    for p in root.rglob("*"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.is_file() and (p.name in COMMAND_FILES or p.parts[-2:-1] == (".github",)):
            try:
                files.append(str(p.relative_to(root)))
            except ValueError:
                continue

    commands = []
    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            for k, v in data.get("scripts", {}).items():
                commands.append({
                    "command": f"npm run {k}",
                    "source": "package.json",
                    "raw": v,
                    "status": "unverified",
                })
        except Exception:
            pass

    make = root / "Makefile"
    if make.exists():
        try:
            txt = make.read_text(errors="ignore")
            for m in re.finditer(r"^([A-Za-z0-9_.-]+):", txt, re.M):
                commands.append({
                    "command": f"make {m.group(1)}",
                    "source": "Makefile",
                    "status": "unverified",
                })
        except Exception:
            pass

    return {
        "files": files,
        "commands": commands,
        "unknowns": [
            "部署流程未确认",
            "生产配置来源未确认",
            "敏感信息边界未确认",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--write", action="store_true", help="write draft files under target root")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    data = discover(root)

    if args.write:
        report = root / "PROJECT_DISCOVERY_REPORT.md"
        report.write_text(
            "# PROJECT DISCOVERY REPORT\n\n"
            "由 `scripts/discover_project.py` 生成。这是 vibe-harness 的只读侦察产物，须人工确认后才能升级到 shadow_harness。\n\n"
            "```json\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```\n",
            encoding="utf-8",
        )
        mb = root / "memory-bank"
        mb.mkdir(exist_ok=True)
        (mb / "architecture.draft.md").write_text(
            "# Architecture Draft\n\n由 discover_project.py 生成，需人工确认后转正。\n",
            encoding="utf-8",
        )
        (mb / "tech-stack.draft.md").write_text(
            "# Tech Stack Draft\n\n```json\n"
            + json.dumps(data["commands"], ensure_ascii=False, indent=2)
            + "\n```\n",
            encoding="utf-8",
        )

    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
