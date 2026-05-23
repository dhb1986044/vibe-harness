#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Install vibe-harness v5.7 into a target repository.

Modes (per docs/agents/project-modes.md):
- bootstrap : new_project - empty repo, full install with managed_harness.
- retrofit  : vibe_managed_legacy - has existing AGENTS/memory-bank/LESSONS; preserve Map split.
- discovery : unmanaged_legacy - read-only first; never overwrite business code or AGENTS.

Hardening:
- Detects Map-style AGENTS.md (links to docs/agents/*.md). Refuses to overwrite it
  unless --overwrite-agents is explicitly passed; writes AGENTS.v5.7.draft.md instead.
- Defaults to a lean skill set and light context profile; pass
  --skill-set full --context-profile full to reproduce the heavier v5.6 shape.
- --dry-run prints intended actions without touching the filesystem.
"""
from __future__ import annotations
import argparse
import re
import shutil
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
MODES = ("bootstrap", "retrofit", "discovery")
CONTEXT_PROFILES = ("light", "standard", "full")
SKILL_SETS = ("lean", "full")

COMMON_PATHS = ["scripts", "docs", "evolution", "memory-bank", "templates"]
FULL_AGENT_PATHS = [".codex", ".claude"]
LEAN_CODEX_SKILLS = [
    "vibe-memory-check",
    "vibe-evolve",
    "vibe-guard",
    "vibe-xcheck",
    "vibe-bootstrap",
    "vibe-retrofit",
    "vibe-discovery",
    "vibe-exec",
    "vibe-plan",
    "vibe-context",
    "vibe-changelog",
    "vibe-lessons",
    "vibe-debug",
    "vibe-review",
]
LEAN_CLAUDE_SKILLS = [
    "vibe-memory-check",
    "vibe-evolve",
    "vibe-guard",
    "vibe-xcheck",
    "vibe-bootstrap",
    "vibe-retrofit",
    "vibe-discovery",
    "vibe-exec",
]
LEAN_COPILOT_SKILLS = ["vibe-memory-check", "vibe-evolve", "vibe-guard", "vibe-xcheck"]
SKIP_DIR_NAMES = {
    ".git",
    ".serena",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
}
SKIP_FILE_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
SKIP_FILE_SUFFIXES = {".pyc", ".pyo"}


def should_skip_copy(path: Path) -> bool:
    if path.name in SKIP_DIR_NAMES or path.name in SKIP_FILE_NAMES:
        return True
    return path.suffix in SKIP_FILE_SUFFIXES


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
    if should_skip_copy(src):
        return
    if dry:
        print(f"COPY {src} -> {dst}")
        return
    if src.is_dir():
        if dst.exists():
            for child in src.iterdir():
                if should_skip_copy(child):
                    continue
                copy_tree(child, dst / child.name, dry)
        else:
            shutil.copytree(src, dst, ignore=lambda current_dir, names: [
                name for name in names if should_skip_copy(Path(current_dir) / name)
            ])
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def copy_if_missing(src: Path, dst: Path, dry: bool, label: str) -> None:
    if not src.exists():
        return
    if dst.exists():
        print(f"{label}: kept existing {dst.relative_to(dst.parents[1]) if len(dst.parents) > 1 else dst.name}")
        return
    if dry:
        print(f"COPY {src} -> {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"{label}: wrote {dst.name}")


def copy_skill_set(target: Path, skill_set: str, dry: bool) -> None:
    if skill_set == "full":
        for rel in FULL_AGENT_PATHS:
            copy_tree(SRC / rel, target / rel, dry)
        return

    # Lean mode installs agent config plus the minimal skill surface used by
    # routine development. It never removes target-owned skills.
    copy_tree(SRC / ".codex" / "hooks.json", target / ".codex" / "hooks.json", dry)
    copy_tree(
        SRC / ".claude" / "settings.example.json",
        target / ".claude" / "settings.example.json",
        dry,
    )
    for name in LEAN_CODEX_SKILLS:
        copy_tree(SRC / ".codex" / "skills" / name, target / ".codex" / "skills" / name, dry)
    for name in LEAN_CLAUDE_SKILLS:
        copy_tree(SRC / ".claude" / "skills" / name, target / ".claude" / "skills" / name, dry)
    for name in LEAN_COPILOT_SKILLS:
        copy_tree(SRC / ".github" / "skills" / name, target / ".github" / "skills" / name, dry)


def set_context_profile(target: Path, profile: str, dry: bool) -> None:
    registry = target / "memory-bank" / "memory-registry.yaml"
    if dry:
        print(f"SET {registry} read_policy.default_profile={profile}")
        return
    if not registry.exists():
        print(f"context profile: registry missing, skip setting default_profile={profile}")
        return
    text = registry.read_text(encoding="utf-8")
    if re.search(r"^(\s{2}default_profile:\s*)[A-Za-z_]+", text, re.M):
        text = re.sub(
            r"^(\s{2}default_profile:\s*)[A-Za-z_]+",
            rf"\g<1>{profile}",
            text,
            count=1,
            flags=re.M,
        )
    else:
        text = re.sub(
            r"^(read_policy:\s*)$",
            rf"\1\n  default_profile: {profile}",
            text,
            count=1,
            flags=re.M,
        )
    registry.write_text(text, encoding="utf-8")
    print(f"context profile: set default_profile={profile}")


def ensure_copilot_governance(target: Path, dry: bool) -> None:
    """Install Copilot governance applyTo instruction without overwriting."""
    src = SRC / ".github" / "instructions" / "governance.instructions.md"
    dst = target / ".github" / "instructions" / "governance.instructions.md"
    copy_if_missing(src, dst, dry, "copilot governance")


def ensure_claude_settings(target: Path, dry: bool) -> None:
    """Enable Claude Stop hook by default when the target has no settings."""
    src = SRC / ".claude" / "settings.example.json"
    dst = target / ".claude" / "settings.json"
    copy_if_missing(src, dst, dry, "claude hooks")


def install_agents(target: Path, mode: str, dry: bool, overwrite: bool) -> None:
    src_agents = SRC / "AGENTS.md"
    dst_agents = target / "AGENTS.md"

    if mode == "discovery":
        draft = target / "AGENTS.v5.7.draft.md"
        copy_tree(src_agents, draft, dry)
        print(f"discovery mode: wrote {draft.name} (no overwrite).")
        return

    if not dst_agents.exists() or mode == "bootstrap":
        copy_tree(src_agents, dst_agents, dry)
        return

    # retrofit on existing AGENTS.md
    if is_map_agents(dst_agents) and not overwrite:
        draft = target / "AGENTS.v5.7.draft.md"
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
        draft = target / "AGENTS.v5.7.draft.md"
        copy_tree(src_agents, draft, dry)
        print(f"retrofit mode: existing AGENTS.md present; wrote {draft.name} for review.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", default=".", help="target repository root")
    ap.add_argument("--mode", choices=MODES, required=True)
    ap.add_argument("--context-profile", choices=CONTEXT_PROFILES, default="light")
    ap.add_argument("--skill-set", choices=SKILL_SETS, default="lean")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--overwrite-agents",
        action="store_true",
        help="force replacing target AGENTS.md (otherwise writes AGENTS.v5.6.draft.md).",
    )
    args = ap.parse_args()

    target = Path(args.target).resolve()
    print(
        "Installing vibe-harness v5.7 -> "
        f"{target} mode={args.mode} context={args.context_profile} "
        f"skills={args.skill_set} dry={args.dry_run}"
    )

    if not target.exists():
        if args.dry_run:
            print(f"MKDIR {target}")
        else:
            target.mkdir(parents=True)

    for rel in COMMON_PATHS:
        copy_tree(SRC / rel, target / rel, args.dry_run)

    copy_skill_set(target, args.skill_set, args.dry_run)

    if args.mode == "bootstrap" and args.skill_set == "full":
        copy_tree(SRC / ".github", target / ".github", args.dry_run)
    ensure_copilot_governance(target, args.dry_run)
    ensure_claude_settings(target, args.dry_run)
    set_context_profile(target, args.context_profile, args.dry_run)

    install_agents(target, args.mode, args.dry_run, args.overwrite_agents)

    print()
    print("Next steps:")
    if args.mode == "discovery":
        print("  1) python scripts/discover_project.py --write")
        print("  2) python scripts/check_memory_consistency.py --warn-only")
        print("  3) python scripts/context_budget.py --profile light --json")
    elif args.mode == "retrofit":
        print("  1) Review AGENTS.v5.7.draft.md (if present) and merge into AGENTS.md.")
        print("  2) Update memory-bank/memory-registry.yaml:")
        print("     project_mode: vibe_managed_legacy")
        print("     harness_phase: shadow_harness   # start in shadow, then soft_gate, then managed")
        print("  3) python scripts/context_budget.py --profile light --json")
        print("  4) python scripts/check_memory_consistency.py --warn-only")
    else:  # bootstrap
        print("  1) Set memory-bank/memory-registry.yaml: project_mode=new_project, harness_phase=managed_harness")
        print("  2) python scripts/context_budget.py --profile light --json")
        print("  3) python scripts/check_memory_consistency.py --strict")

    return 0


if __name__ == "__main__":
    sys.exit(main())
