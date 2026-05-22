#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Install vibe-harness v5.6 into a target repository.

Modes (per docs/agents/project-modes.md):
- bootstrap : new_project        — empty repo, full install with managed_harness.
- retrofit  : vibe_managed_legacy — has existing AGENTS/memory-bank/LESSONS; preserve Map split.
- discovery : unmanaged_legacy   — read-only first; never overwrite business code or AGENTS.

Hardening:
- Detects Map-style AGENTS.md (links to docs/agents/*.md). Refuses to overwrite it
  unless --overwrite-agents is explicitly passed; writes AGENTS.v5.6.draft.md instead.
- --dry-run prints intended actions without touching the filesystem.
"""
from __future__ import annotations
import argparse
import shutil
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
MODES = ("bootstrap", "retrofit", "discovery")

COMMON_PATHS = ["scripts", "docs", "evolution", "memory-bank", ".codex", ".claude", "templates"]


def is_map_agents(p: Path) -> bool:
    """Return True if existing AGENTS.md already uses the v5.5+ Map structure."""
    if not p.exists():
        return False
    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    return ("docs/agents/" in txt) and ("memory-bank" in txt)


def copy_tree(src: Path, dst: Path, dry: bool) -> None:
    if not src.exists():
        return
    if dry:
        print(f"COPY {src} -> {dst}")
        return
    if src.is_dir():
        if dst.exists():
            for child in src.iterdir():
                copy_tree(child, dst / child.name, dry)
        else:
            shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def install_agents(target: Path, mode: str, dry: bool, overwrite: bool) -> None:
    src_agents = SRC / "AGENTS.md"
    dst_agents = target / "AGENTS.md"

    if mode == "discovery":
        draft = target / "AGENTS.v5.6.draft.md"
        copy_tree(src_agents, draft, dry)
        print(f"discovery mode: wrote {draft.name} (no overwrite).")
        return

    if not dst_agents.exists() or mode == "bootstrap":
        copy_tree(src_agents, dst_agents, dry)
        return

    # retrofit on existing AGENTS.md
    if is_map_agents(dst_agents) and not overwrite:
        draft = target / "AGENTS.v5.6.draft.md"
        copy_tree(src_agents, draft, dry)
        print(
            f"retrofit mode: existing AGENTS.md detected as Map-style; "
            f"wrote {draft.name} instead. Review and merge manually. "
            f"Pass --overwrite-agents to force replacement."
        )
        return

    if overwrite:
        copy_tree(src_agents, dst_agents, dry)
    else:
        draft = target / "AGENTS.v5.6.draft.md"
        copy_tree(src_agents, draft, dry)
        print(f"retrofit mode: existing AGENTS.md present; wrote {draft.name} for review.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", default=".", help="target repository root")
    ap.add_argument("--mode", choices=MODES, required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--overwrite-agents",
        action="store_true",
        help="force replacing target AGENTS.md (otherwise writes AGENTS.v5.6.draft.md).",
    )
    args = ap.parse_args()

    target = Path(args.target).resolve()
    print(f"Installing vibe-harness v5.6 -> {target} mode={args.mode} dry={args.dry_run}")

    if not target.exists():
        if args.dry_run:
            print(f"MKDIR {target}")
        else:
            target.mkdir(parents=True)

    for rel in COMMON_PATHS:
        copy_tree(SRC / rel, target / rel, args.dry_run)

    if args.mode == "bootstrap":
        copy_tree(SRC / ".github", target / ".github", args.dry_run)

    install_agents(target, args.mode, args.dry_run, args.overwrite_agents)

    print()
    print("Next steps:")
    if args.mode == "discovery":
        print("  1) python scripts/discover_project.py --write")
        print("  2) python scripts/check_memory_consistency.py --warn-only")
    elif args.mode == "retrofit":
        print("  1) Review AGENTS.v5.6.draft.md (if present) and merge into AGENTS.md.")
        print("  2) Update memory-bank/memory-registry.yaml:")
        print("     project_mode: vibe_managed_legacy")
        print("     harness_phase: shadow_harness   # start in shadow, then soft_gate, then managed")
        print("  3) python scripts/check_memory_consistency.py --warn-only")
    else:  # bootstrap
        print("  1) Set memory-bank/memory-registry.yaml: project_mode=new_project, harness_phase=managed_harness")
        print("  2) python scripts/check_memory_consistency.py --strict")

    return 0


if __name__ == "__main__":
    sys.exit(main())
