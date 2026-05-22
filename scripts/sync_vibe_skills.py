#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mirror governance vibe-* skills from .claude/skills to .codex/skills and .github/skills.

Single-source policy applies ONLY to the 4 governance skills:
  vibe-memory-check, vibe-guard, vibe-xcheck, vibe-evolve
.claude/skills/vibe-* is the source of truth for these 4 skills.
.codex/skills/vibe-* and .github/skills/vibe-* must contain byte-identical
copies so Codex, Claude, and Copilot agents see the same governance behaviour.

Other vibe-* skills that exist only in .codex/skills/ (e.g. vibe-init,
vibe-plan, vibe-alpha, vibe-omega, vibe-pipeline, vibe-changelog, vibe-lessons,
vibe-review, vibe-debug, vibe-knowledge, vibe-context, vibe-git) are NOT
mirrored and NOT checked here.

Modes:
  --check  Exit non-zero if any governance mirror is out of sync.
  --write  Make the 4 governance skills in every mirror match .claude/skills exactly.

This script intentionally uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import filecmp
import hashlib
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path.cwd()
SOURCE = ROOT / ".claude" / "skills"
# Mirrors: {label: absolute Path}. Adding a new agent target = one entry here.
MIRRORS: Dict[str, Path] = {
    "codex": ROOT / ".codex" / "skills",
    "copilot": ROOT / ".github" / "skills",
}
# Backwards compat alias for older callers / tests.
MIRROR = MIRRORS["codex"]
SKILL_PREFIX = "vibe-"
GOVERNED_SKILLS = ("vibe-memory-check", "vibe-guard", "vibe-xcheck", "vibe-evolve")


def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def collect_vibe_files(root: Path) -> List[Path]:
    """Collect contract files from the 4 governed skills.

    Only files NOT under a ``docs/`` subdirectory are considered part of the
    contract. Each side may extend its own ``docs/`` (e.g. harness-creator
    adds richer docs/ to .codex/skills/) without breaking the governance
    contract.
    """
    if not root.exists():
        return []
    out: List[Path] = []
    for name in GOVERNED_SKILLS:
        skill_dir = root / name
        if not skill_dir.is_dir():
            continue
        for p in skill_dir.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(skill_dir)
            if rel.parts and rel.parts[0] == "docs":
                continue  # docs/ is allowed to diverge per-side
            out.append(p)
    return out


def diff_one(mirror_root: Path) -> Tuple[List[Path], List[Path], List[Path]]:
    """Return (missing, different, extra) for one mirror root."""
    src_files = {p.relative_to(SOURCE): p for p in collect_vibe_files(SOURCE)}
    mir_files = {p.relative_to(mirror_root): p for p in collect_vibe_files(mirror_root)}

    missing: List[Path] = []
    different: List[Path] = []
    extra: List[Path] = []

    for rel, src in src_files.items():
        mir = mir_files.get(rel)
        if mir is None:
            missing.append(rel)
        elif file_hash(src) != file_hash(mir):
            different.append(rel)

    for rel in mir_files:
        if rel not in src_files:
            extra.append(rel)

    return missing, different, extra


def diff() -> Tuple[List[Path], List[Path], List[Path]]:
    """Backwards-compatible aggregator over all mirrors.

    Returns the *union* of (missing, different, extra) across mirrors so
    legacy callers (e.g. ``check_memory_consistency.check_referenced_paths``)
    continue to work without per-mirror awareness.
    """
    all_missing: List[Path] = []
    all_different: List[Path] = []
    all_extra: List[Path] = []
    for mirror_root in MIRRORS.values():
        m, d, e = diff_one(mirror_root)
        for rel in m:
            if rel not in all_missing:
                all_missing.append(rel)
        for rel in d:
            if rel not in all_different:
                all_different.append(rel)
        for rel in e:
            if rel not in all_extra:
                all_extra.append(rel)
    return all_missing, all_different, all_extra


def cmd_check() -> int:
    if not SOURCE.exists():
        print(f"FAIL: source missing: {SOURCE}", file=sys.stderr)
        return 2
    any_bad = False
    for label, mirror_root in MIRRORS.items():
        missing, different, extra = diff_one(mirror_root)
        rel_root = mirror_root.relative_to(ROOT).as_posix()
        if not (missing or different or extra):
            print(
                "PASS: governance vibe-* skills ("
                + ", ".join(GOVERNED_SKILLS)
                + f") in {rel_root} ({label}) are in sync with .claude/skills/"
            )
            continue
        any_bad = True
        print(f"FAIL: {label} mirror out of sync ({rel_root}):", file=sys.stderr)
        for rel in missing:
            print(f"  missing in mirror: {rel.as_posix()}", file=sys.stderr)
        for rel in different:
            print(f"  content differs:   {rel.as_posix()}", file=sys.stderr)
        for rel in extra:
            print(f"  extra in mirror:   {rel.as_posix()}", file=sys.stderr)
    if any_bad:
        print(
            "\nFix: run `python scripts/sync_vibe_skills.py --write` to rebuild "
            "all governance mirrors from .claude/skills.",
            file=sys.stderr,
        )
        return 1
    return 0


def _write_mirror(label: str, mirror_root: Path) -> int:
    """Rebuild one mirror from SOURCE. Returns 0 on success, 3 on residual drift."""
    # 1. Remove governed vibe-* dirs that no longer exist in source.
    if mirror_root.exists():
        for name in GOVERNED_SKILLS:
            mir_dir = mirror_root / name
            src_dir = SOURCE / name
            if mir_dir.exists() and not src_dir.exists():
                shutil.rmtree(mir_dir)
                print(f"removed: {mir_dir.relative_to(ROOT).as_posix()} ({label})")

    # 2. Copy each governed vibe-* skill from source to mirror, but preserve
    # any per-mirror ``docs/`` subdirectory (allowed to diverge per side).
    mirror_root.mkdir(parents=True, exist_ok=True)
    for name in GOVERNED_SKILLS:
        skill_dir = SOURCE / name
        if not skill_dir.is_dir():
            continue
        dst = mirror_root / skill_dir.name
        docs_backup = None
        existing_docs = dst / "docs"
        if existing_docs.exists():
            docs_backup = dst.parent / f".{dst.name}.docs.bak"
            if docs_backup.exists():
                shutil.rmtree(docs_backup)
            shutil.move(str(existing_docs), str(docs_backup))
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(skill_dir, dst)
        # If source has no docs/ of its own, restore preserved mirror-side docs/.
        if docs_backup is not None:
            src_docs = skill_dir / "docs"
            if not src_docs.exists():
                shutil.move(str(docs_backup), str(dst / "docs"))
            else:
                shutil.rmtree(docs_backup)
        print(f"mirrored: {dst.relative_to(ROOT).as_posix()} ({label})")

    # 3. Verify.
    missing, different, extra = diff_one(mirror_root)
    if missing or different or extra:
        print(f"ERROR: {label} mirror still out of sync after write", file=sys.stderr)
        return 3
    return 0


def cmd_write() -> int:
    if not SOURCE.exists():
        print(f"FAIL: source missing: {SOURCE}", file=sys.stderr)
        return 2
    rc = 0
    for label, mirror_root in MIRRORS.items():
        rc = _write_mirror(label, mirror_root) or rc
    if rc == 0:
        print("PASS: all mirrors rebuilt and verified")
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="exit non-zero if out of sync")
    g.add_argument("--write", action="store_true", help="rebuild mirror from source")
    args = parser.parse_args()
    return cmd_check() if args.check else cmd_write()


if __name__ == "__main__":
    sys.exit(main())
