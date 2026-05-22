#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, shutil, sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]

MODES = {"bootstrap", "retrofit", "discovery"}

def copy_tree(src: Path, dst: Path, dry=False):
    if not src.exists(): return
    if dry:
        print(f"COPY {src} -> {dst}")
        return
    if dst.exists() and src.is_dir():
        for child in src.iterdir():
            copy_tree(child, dst/child.name, dry)
    elif src.is_dir():
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--target', required=True)
    ap.add_argument('--mode', choices=sorted(MODES), required=True)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--overwrite-agents', action='store_true')
    args=ap.parse_args()
    target=Path(args.target).resolve()
    print(f"Installing vibe-harness v5.1 to {target} mode={args.mode} dry={args.dry_run}")
    if not target.exists():
        if args.dry_run: print(f"MKDIR {target}")
        else: target.mkdir(parents=True)
    # core dirs
    for name in ['scripts','manuals','docs','evolution','memory-bank','.codex','.claude','templates']:
        copy_tree(SRC/name, target/name, args.dry_run)
    # AGENTS policy
    ag=target/'AGENTS.md'
    if args.mode=='bootstrap' or args.overwrite_agents or not ag.exists():
        copy_tree(SRC/'AGENTS.md', ag, args.dry_run)
    else:
        dst=target/'AGENTS.v5.1.draft.md'
        copy_tree(SRC/'AGENTS.md', dst, args.dry_run)
        print('Existing AGENTS.md detected; wrote AGENTS.v5.1.draft.md instead. Review before replacing.')
    if args.mode=='discovery':
        print('Next: run python scripts/discover_project.py --write')
    print('Next: run python scripts/check_memory_consistency.py --warn-only')
    return 0
if __name__=='__main__':
    raise SystemExit(main())
