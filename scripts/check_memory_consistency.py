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
from datetime import date as _date

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

# v5.1: AGENTS.md Map 拆分后的子文档。缺失这些文件意味着 AGENTS.md 的链接断裂。
AGENTS_SUBDOCS = [
    "docs/agents/lifecycle.md",
    "docs/agents/memory-model.md",
    "docs/agents/lessons-policy.md",
    "docs/agents/evolution-policy.md",
    "docs/agents/safety-and-completion.md",
    "docs/agents/hooks-and-commands.md",
]

# v5.1: vibe-* 治理 skill 单源在 .claude/skills，.codex/skills 与 .github/skills 为镜像。
# v5.5: copilot 第三镜像 (.github/skills) 加入；sync_vibe_skills.py 已扩展为三向同步。
VIBE_SKILLS_SOURCE = ".claude/skills"
VIBE_SKILLS_MIRRORS = (".codex/skills", ".github/skills")
# Backwards-compat alias used by older log strings.
VIBE_SKILLS_MIRROR = ".codex/skills"
VIBE_SKILL_NAMES = ["vibe-memory-check", "vibe-evolve", "vibe-guard", "vibe-xcheck"]

COPILOT_GOVERNANCE_INSTRUCTION = ".github/instructions/governance.instructions.md"
COPILOT_GOVERNANCE_APPLY_TO_REQUIRED = [
    "memory-bank/**",
    "docs/LESSONS*.md",
    "docs/AI_CHANGELOG.md",
    "docs/agents/**",
    "evolution/**",
    "AGENTS.md",
    ".claude/skills/vibe-*/**",
    ".codex/skills/vibe-*/**",
    ".github/skills/vibe-*/**",
    ".github/instructions/**",
    ".github/copilot-instructions.md",
    "scripts/hooks/**",
    "scripts/sync_vibe_skills.py",
    "scripts/check_memory_consistency.py",
    "scripts/context_budget.py",
    "scripts/evolve_lessons.py",
]

STATUS_ALLOWED = {"活跃", "已归档", "Pinned", "active", "archived", "pinned"}

# v5.6: 项目模式与 harness 阶段（来自 v5.1 增量整合）。
# 解析自 memory-bank/memory-registry.yaml 的 project_mode / harness_phase 字段。
PROJECT_MODES = {"new_project", "vibe_managed_legacy", "unmanaged_legacy"}
HARNESS_PHASES = {"discovery_only", "shadow_harness", "soft_gate", "managed_harness"}
DEFAULT_PROJECT_MODE = "unmanaged_legacy"
DEFAULT_HARNESS_PHASE = "discovery_only"

# v5.2: lesson schema — type (5-class MECE) and maturity (3-level).
LESSON_TYPES = {"model", "decision", "guideline", "pitfall", "process"}
LESSON_MATURITIES = {"draft", "verified", "proven"}

# v5.3: reference-tracking scan targets. Lessons referenced in these files
# count toward `last_referenced` / `reference_count` in lesson-index.json.
# LESSONS.md / LESSONS_ARCHIVE.md / lesson-index.json itself are excluded to
# avoid counting self-references.
LESSON_REF_SCAN_FILES = [
    "memory-bank/progress.md",
    "memory-bank/activeContext.md",
    "memory-bank/architecture.md",
    "docs/AI_CHANGELOG.md",
    "evolution/promotion-log.md",
]
LESSON_REF_SCAN_GLOBS = [
    "plans/*.md",
    "plans/**/*.md",
]
# Long-unused thresholds (months) for active-window warnings.
LESSON_UNUSED_VERIFIED_MONTHS = 6
LESSON_UNUSED_PROVEN_MONTHS = 12

# v5.4: chronological-log heading prefix lint.
# Files that record dated entries SHOULD use parseable heading format
#   ## [YYYY-MM-DD] <kind> | <summary>
# so `grep "^## \[" <file> | tail -5` reliably extracts the recent timeline.
# Inspired by Karpathy's LLM-Wiki gist (log.md convention).
LOG_PREFIX_FILES = {
    "docs/AI_CHANGELOG.md": "changelog",
    "evolution/promotion-log.md": "promote",
    "memory-bank/progress.md": "progress",
}
LOG_PREFIX_KINDS = {"changelog", "promote", "lint", "progress", "evolve", "ingest", "decision"}
LOG_PREFIX_RE = re.compile(
    r"^##\s+\[(\d{4}-\d{2}-\d{2})\]\s+([a-z]+)\s+\|\s+\S"
)
# Any `## ` heading whose content starts with a YYYY-MM-DD date (in any form)
# but does not match LOG_PREFIX_RE should be flagged.
LOG_DATE_HEADING_RE = re.compile(r"^##\s+.*\b20\d{2}-[01]\d-[0-3]\d\b")

# Date pattern used to anchor "when was this lesson last referenced":
# we look for ISO-like dates near a `L\d+` mention within the same file.
DATE_RE = re.compile(r"\b(20\d{2}-[01]\d-[0-3]\d)\b")
LESSON_REF_RE = re.compile(r"\bL(\d+)\b")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_registry_phase() -> Tuple[str, str]:
    """v5.6: 读取 memory-registry.yaml 的 project_mode + harness_phase。

    返回 (project_mode, harness_phase)；任一字段缺失或无效时回落到默认值
    (unmanaged_legacy, discovery_only) —— 与 v5.1 安装器对 "registry 不存在"
    的处理保持一致：未声明 = 视为纯人工历史项目，最保守的 warn-only 行为。
    """
    p = ROOT / "memory-bank/memory-registry.yaml"
    if not p.exists():
        return DEFAULT_PROJECT_MODE, DEFAULT_HARNESS_PHASE
    text = p.read_text(encoding="utf-8")
    mode_m = re.search(r"^project_mode:\s*([A-Za-z_]+)", text, re.M)
    phase_m = re.search(r"^harness_phase:\s*([A-Za-z_]+)", text, re.M)
    mode = mode_m.group(1).strip() if mode_m else DEFAULT_PROJECT_MODE
    phase = phase_m.group(1).strip() if phase_m else DEFAULT_HARNESS_PHASE
    if mode not in PROJECT_MODES:
        mode = DEFAULT_PROJECT_MODE
    if phase not in HARNESS_PHASES:
        phase = DEFAULT_HARNESS_PHASE
    return mode, phase


def parse_lessons_index(text: str) -> Dict[str, Dict[str, str]]:
    """Parse the `## 索引` table.

    Supports both legacy 5-column format (#, 标题, 标签, 优先级, 状态) and
    v5.2 7-column format (#, 标题, 类型, 成熟度, 标签, 优先级, 状态).
    Missing columns default to empty string so callers can treat them as
    "unset" and emit a schema warning rather than crash.
    """
    rows: Dict[str, Dict[str, str]] = {}
    in_index = False
    header_cols: List[str] = []
    for line in text.splitlines():
        if line.strip() == "## 索引":
            in_index = True
            continue
        if in_index and line.startswith("## "):
            break
        if not in_index:
            continue
        if not line.startswith("|"):
            continue
        if "---" in line:
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        # Header row: capture column names so we can map by position.
        if cols and cols[0] == "#":
            header_cols = cols
            continue
        if not cols or not re.fullmatch(r"L\d+", cols[0]):
            continue
        # Map columns by header name when available; otherwise fall back to
        # legacy fixed positions.
        row: Dict[str, str] = {"title": "", "type": "", "maturity": "",
                                "tags": "", "priority": "", "status": ""}
        if header_cols and len(header_cols) == len(cols):
            for name, value in zip(header_cols, cols):
                if name == "标题":
                    row["title"] = value
                elif name == "类型":
                    row["type"] = value
                elif name == "成熟度":
                    row["maturity"] = value
                elif name == "标签":
                    row["tags"] = value
                elif name == "优先级":
                    row["priority"] = value
                elif name == "状态":
                    row["status"] = value
        else:
            # Legacy 5-col fallback.
            if len(cols) >= 5:
                row["title"], row["tags"], row["priority"], row["status"] = cols[1], cols[2], cols[3], cols[4]
        rows[cols[0]] = row
    return rows


def parse_lesson_bodies(text: str) -> Dict[str, Dict[str, str]]:
    """Parse `## L{n}` section bodies for `- 类型：` and `- 成熟度：` fields."""
    bodies: Dict[str, Dict[str, str]] = {}
    current: str = ""
    for line in text.splitlines():
        m = re.match(r"^##\s+(L\d+)\b", line)
        if m:
            current = m.group(1)
            bodies.setdefault(current, {})
            continue
        if not current:
            continue
        m_type = re.match(r"^-\s*类型\s*[:：]\s*(\S+)", line)
        if m_type:
            bodies[current]["type"] = m_type.group(1).strip()
            continue
        m_mat = re.match(r"^-\s*成熟度\s*[:：]\s*(\S+)", line)
        if m_mat:
            bodies[current]["maturity"] = m_mat.group(1).strip()
    return bodies


def parse_lesson_headings(text: str) -> List[str]:
    return re.findall(r"^##\s+(L\d+)\b", text, flags=re.M)


def scan_lesson_refs(known_ids: set) -> Dict[str, Dict[str, object]]:
    """v5.3 reference-tracking scanner.

    Walks ``LESSON_REF_SCAN_FILES`` + ``LESSON_REF_SCAN_GLOBS`` and finds
    every ``L\\d+`` mention whose id is in ``known_ids``. For each lesson id
    we record:

    - ``count``: total occurrences across all scanned files.
    - ``last_referenced``: the latest ISO date (YYYY-MM-DD) that appears in
      the same scanned file as the mention. Date anchors are inherited from
      the nearest preceding ``## 20xx-xx-xx`` heading (or any ISO date on
      the same line). This is intentionally approximate — the goal is
      "rough recency", not audit-grade provenance.
    - ``sources``: deduplicated list of files the lesson was mentioned in.

    Returns ``{lesson_id: {count, last_referenced, sources}}`` for every
    known lesson, including those with zero references (count=0, last=None).
    """
    out: Dict[str, Dict[str, object]] = {
        lid: {"count": 0, "last_referenced": None, "sources": []} for lid in known_ids
    }

    files: List[Path] = []
    for rel in LESSON_REF_SCAN_FILES:
        p = ROOT / rel
        if p.exists():
            files.append(p)
    for pattern in LESSON_REF_SCAN_GLOBS:
        files.extend(sorted(ROOT.glob(pattern)))

    seen: set = set()
    for path in files:
        if path in seen:
            continue
        seen.add(path)
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = path.relative_to(ROOT).as_posix()
        # Walk line-by-line so we can carry a "current date context" forward.
        current_date: str = ""
        for line in text.splitlines():
            # Date heading like "## 2026-05-12" updates the date context.
            date_match = DATE_RE.search(line)
            if date_match:
                current_date = date_match.group(1)
            for m in LESSON_REF_RE.finditer(line):
                lid = "L" + m.group(1)
                if lid not in out:
                    continue
                entry = out[lid]
                entry["count"] = int(entry["count"]) + 1  # type: ignore[assignment]
                if rel not in entry["sources"]:  # type: ignore[operator]
                    entry["sources"].append(rel)  # type: ignore[union-attr]
                if current_date:
                    prev = entry["last_referenced"]
                    if prev is None or current_date > prev:
                        entry["last_referenced"] = current_date
    return out


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


def actionable(what: str, why: str, how: List[str]) -> str:
    """Format an error per harness-creator standard: WHAT + WHY + HOW.

    Linter errors must be agent-actionable so the agent (or human) can fix
    the problem without further context-switching.
    """
    how_block = "\n".join(f"         {i + 1}) {h}" for i, h in enumerate(how))
    return f"{what}\n         WHY:  {why}\n         HOW:\n{how_block}"


def parse_frontmatter_value(text: str, key: str) -> str:
    """Return a simple one-line YAML frontmatter value without a YAML dependency."""
    in_frontmatter = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if lineno == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter and stripped == "---":
            break
        if in_frontmatter and line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def check_referenced_paths() -> List[str]:
    """v5.1 L2 reference-integrity check.

    Verifies that paths referenced by harness-governance documents really
    exist on disk. Without this check, renaming or deleting a vibe-* skill,
    a hook script, or a registry-listed file leaves the harness silently
    broken until a real task hits the missing reference.
    """
    errors: List[str] = []

    # 1. AGENTS.md Map subdocs must exist; otherwise navigation links rot.
    for rel in AGENTS_SUBDOCS:
        if not (ROOT / rel).exists():
            errors.append(actionable(
                what=f"AGENTS.md subdoc missing: {rel}",
                why="AGENTS.md (Map) links to docs/agents/*.md for detailed contract; "
                    "a missing subdoc means the navigation Map is broken.",
                how=[
                    f"Create {rel} from AGENTS.legacy.md content",
                    "Or remove the corresponding link from AGENTS.md if the section was intentionally dropped",
                ],
            ))

    # 2. Required vibe-* skills must exist in source AND every registered mirror.
    src_root = ROOT / VIBE_SKILLS_SOURCE
    mirror_roots = [ROOT / m for m in VIBE_SKILLS_MIRRORS]
    for name in VIBE_SKILL_NAMES:
        src_skill = src_root / name / "SKILL.md"
        if not src_skill.exists():
            errors.append(actionable(
                what=f"vibe-* skill source missing: {src_skill.relative_to(ROOT).as_posix()}",
                why=f"{name} is listed in memory-registry.yaml required_vibe_skills "
                    "and must exist in the .claude/skills single-source root.",
                how=[
                    f"Create {src_skill.relative_to(ROOT).as_posix()}",
                    f"Or remove {name} from memory-registry.yaml required_vibe_skills",
                ],
            ))
        for mir_root in mirror_roots:
            mir_skill = mir_root / name / "SKILL.md"
            if not mir_skill.exists():
                errors.append(actionable(
                    what=f"vibe-* skill mirror missing: {mir_skill.relative_to(ROOT).as_posix()}",
                    why=f"{mir_root.relative_to(ROOT).as_posix()}/vibe-* must mirror "
                        ".claude/skills/vibe-* so all agents (Codex / Claude / Copilot) "
                        "see the same governance behaviour.",
                    how=[
                        "Run `python scripts/sync_vibe_skills.py --write` to rebuild every mirror",
                        f"Or create {mir_skill.relative_to(ROOT).as_posix()} manually",
                    ],
                ))

    # 3. vibe-* mirrors must be byte-identical to source (per registered mirror).
    if src_root.exists() and any(r.exists() for r in mirror_roots):
        try:
            import sys as _sys
            _sys.path.insert(0, str(ROOT / "scripts"))
            try:
                from sync_vibe_skills import diff_one as _diff_one, MIRRORS as _MIRRORS  # type: ignore
                for label, mir_root in _MIRRORS.items():
                    missing, different, extra = _diff_one(mir_root)
                    if not (missing or different or extra):
                        continue
                    detail = []
                    for rel in missing:
                        detail.append(f"missing in {label} mirror: {rel.as_posix()}")
                    for rel in different:
                        detail.append(f"content differs in {label}: {rel.as_posix()}")
                    for rel in extra:
                        detail.append(f"extra in {label} mirror: {rel.as_posix()}")
                    errors.append(actionable(
                        what=f"vibe-* {label} mirror out of sync with .claude/skills source: "
                             + "; ".join(detail),
                        why="Single-source policy requires every vibe-* governance mirror "
                            "(.codex/skills, .github/skills) to be byte-identical to "
                            ".claude/skills/vibe-*. Drift means Codex / Claude / Copilot "
                            "agents see different governance rules.",
                        how=[
                            "Run `python scripts/sync_vibe_skills.py --write` to rebuild every mirror",
                            "If you intended a divergence, update the single-source policy in AGENTS.md §12 first",
                        ],
                    ))
            finally:
                _sys.path.pop(0)
        except Exception as exc:
            errors.append(f"failed to invoke sync_vibe_skills.diff_one(): {exc}")

    # 4. SKILL.md files in the source must reference scripts that actually exist.
    if src_root.exists():
        cmd_pattern = re.compile(r"python\s+(scripts/[\w/.\-]+\.py)")
        for skill_dir in sorted(src_root.iterdir()):
            if not skill_dir.is_dir() or not skill_dir.name.startswith("vibe-"):
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            for match in cmd_pattern.finditer(skill_md.read_text(encoding="utf-8")):
                script_rel = match.group(1)
                if not (ROOT / script_rel).exists():
                    errors.append(actionable(
                        what=f"{skill_md.relative_to(ROOT).as_posix()} references missing script: {script_rel}",
                        why="SKILL.md commands must point to scripts that exist; otherwise "
                            "the skill cannot execute when invoked.",
                        how=[
                            f"Create {script_rel}",
                            f"Or update {skill_md.relative_to(ROOT).as_posix()} to point to the real script path",
                        ],
                    ))

    # 5. memory-registry.yaml `checks.*` commands must reference real scripts.
    registry = ROOT / "memory-bank/memory-registry.yaml"
    if registry.exists():
        text = registry.read_text(encoding="utf-8")
        for match in re.finditer(r"python\s+(scripts/[\w/.\-]+\.py)", text):
            script_rel = match.group(1)
            if not (ROOT / script_rel).exists():
                errors.append(actionable(
                    what=f"memory-registry.yaml references missing script: {script_rel}",
                    why="`checks.*` and similar fields must point to scripts that exist; "
                        "otherwise the harness contract is silently broken.",
                    how=[
                        f"Create {script_rel}",
                        "Or update memory-registry.yaml to remove/rename the broken reference",
                    ],
                ))

    # 6. Copilot governance applyTo instruction must exist and cover the
    # governance paths described by AGENTS.md / memory-registry.yaml.
    copilot_entry = ROOT / ".github" / "copilot-instructions.md"
    governance_instruction = ROOT / COPILOT_GOVERNANCE_INSTRUCTION
    governance_declared = (
        copilot_entry.exists()
        or (registry.exists() and COPILOT_GOVERNANCE_INSTRUCTION in registry.read_text(encoding="utf-8", errors="ignore"))
        or (registry.exists() and ".github/instructions/" in registry.read_text(encoding="utf-8", errors="ignore"))
    )
    if governance_declared and not governance_instruction.exists():
        errors.append(actionable(
            what=f"Copilot governance instruction missing: {COPILOT_GOVERNANCE_INSTRUCTION}",
            why="AGENTS.md and memory-registry.yaml describe Copilot's governance-face applyTo "
                "safety net. If the file is absent, Copilot loses the passive MEMORY_CHECK / "
                "sync reminder for governance edits.",
            how=[
                "Copy .github/instructions/governance.instructions.md from the harness source",
                "Or remove the Copilot applyTo references from AGENTS.md / memory-registry.yaml if Copilot is intentionally unsupported",
            ],
        ))
    elif governance_instruction.exists():
        gov_text = governance_instruction.read_text(encoding="utf-8", errors="ignore")
        apply_to = parse_frontmatter_value(gov_text, "applyTo")
        if not apply_to:
            errors.append(actionable(
                what=f"{COPILOT_GOVERNANCE_INSTRUCTION} missing frontmatter `applyTo`",
                why="GitHub Copilot only loads this instruction automatically when applyTo matches touched files.",
                how=["Add an `applyTo` value covering the governance paths in memory-registry.yaml"],
            ))
        else:
            missing_apply_to = [p for p in COPILOT_GOVERNANCE_APPLY_TO_REQUIRED if p not in apply_to]
            if missing_apply_to:
                errors.append(actionable(
                    what=f"{COPILOT_GOVERNANCE_INSTRUCTION} applyTo misses governance paths: "
                         + ", ".join(missing_apply_to),
                    why="Copilot has no shell Stop hook; missing applyTo coverage means some governance edits "
                        "won't receive the passive MEMORY_CHECK / sync reminder.",
                    how=[
                        f"Add the missing path patterns to `{COPILOT_GOVERNANCE_INSTRUCTION}` frontmatter",
                        "Keep the list semantically aligned with memory-registry.yaml `governance_paths`",
                    ],
                ))

    # 7. v5.1 ghost-file linter (lesson L5 candidate).
    # vibe-* skills (SKILL.md + docs/) must not reference deprecated ghost
    # files or directories that were removed during the v5.1 cleanup. Lines
    # that explicitly forbid the ghost (negation context) are allowed because
    # they ARE the contract banning the ghost.
    GHOST_PATTERNS = [
        ("PROJECT_GUIDE", "PROJECT_GUIDE.md was removed; sink decisions to memory-bank/architecture.md (ADR) or docs/LESSONS.md."),
        ("briefing.md", "briefing.md is not registered in memory-registry.yaml; append to memory-bank/activeContext.md instead."),
        ("open_questions.md", "open_questions.md is not registered in memory-registry.yaml; append to memory-bank/activeContext.md instead."),
    ]
    NEGATION_CONTEXT = (
        "不创建", "不引用", "禁止创建", "禁止引用", "未注册", "幽灵", "已废弃",
        "removed", "deprecated", "do not create", "must not", "ghost",
    )
    skill_roots = [ROOT / VIBE_SKILLS_SOURCE] + [ROOT / m for m in VIBE_SKILLS_MIRRORS]
    for skill_root in skill_roots:
        if not skill_root.exists():
            continue
        for md_path in skill_root.rglob("*.md"):
            try:
                lines = md_path.read_text(encoding="utf-8").splitlines()
            except Exception:
                continue
            for lineno, line in enumerate(lines, start=1):
                for ghost, advice in GHOST_PATTERNS:
                    if ghost not in line:
                        continue
                    if any(neg in line for neg in NEGATION_CONTEXT):
                        continue
                    rel = md_path.relative_to(ROOT).as_posix()
                    errors.append(actionable(
                        what=f"ghost-file reference in {rel}:{lineno} -> '{ghost}'",
                        why=advice,
                        how=[
                            f"Edit {rel}:{lineno} to remove the ghost reference",
                            "Or rephrase the line as an explicit ban (negation context) so the linter accepts it",
                        ],
                    ))

    return errors


def check_orphan_docs() -> List[str]:
    """v5.4 orphan-page linter (Karpathy LLM-Wiki Lint inspiration).

    Two-way binding between catalog and content:

    1. Every ``docs/agents/*.md`` file must appear at least once in
       ``AGENTS.md`` (the Map). A subdoc that nothing links to is an
       orphan — readers can't find it and it silently rots.
    2. Every ``memory-bank/*.md`` file (excluding the registry itself and
       optional ``prd.md``) must appear at least once in
       ``memory-bank/memory-registry.yaml`` (the catalog). Files not
       cataloged won't be bootstrap-loaded.

    Returns WARN-grade messages (callers append to warnings, not errors)
    so external template forks aren't broken on import — orphans are a
    hygiene issue, not a correctness issue.
    """
    warnings_out: List[str] = []

    agents_md = ROOT / "AGENTS.md"
    agents_text = read(agents_md)
    if agents_text:
        agents_dir = ROOT / "docs/agents"
        if agents_dir.exists():
            for md in sorted(agents_dir.glob("*.md")):
                rel = md.relative_to(ROOT).as_posix()
                if rel not in agents_text:
                    warnings_out.append(actionable(
                        what=f"orphan docs/agents page: {rel} is not referenced in AGENTS.md",
                        why="docs/agents/*.md files are Reference content for AGENTS.md (Map). "
                            "A page not linked from the Map is invisible to bootstrap readers.",
                        how=[
                            f"Link {rel} from AGENTS.md (typically in §12 navigation or relevant section)",
                            f"Or delete {rel} if it is no longer needed",
                        ],
                    ))

    registry = ROOT / "memory-bank/memory-registry.yaml"
    registry_text = read(registry)
    if registry_text:
        mb_dir = ROOT / "memory-bank"
        if mb_dir.exists():
            skip = {"memory-registry.yaml"}
            for md in sorted(mb_dir.glob("*.md")):
                if md.name in skip:
                    continue
                rel = md.relative_to(ROOT).as_posix()
                if rel not in registry_text:
                    warnings_out.append(actionable(
                        what=f"orphan memory-bank file: {rel} is not cataloged in memory-registry.yaml",
                        why="memory-bank/*.md files are project facts; un-cataloged files won't be "
                            "loaded during MEMORY_BOOTSTRAP and silently rot.",
                        how=[
                            f"Add {rel} under `core_files` or `read_policy.bootstrap_order` in memory-registry.yaml",
                            f"Or delete {rel} if it is no longer needed",
                        ],
                    ))

    return warnings_out


def check_log_prefix() -> List[str]:
    """v5.4 chronological-log prefix linter (Karpathy LLM-Wiki Lint inspiration).

    Scans ``LOG_PREFIX_FILES`` for ``## `` headings that look like dated
    entries but don't match the parseable format
    ``## [YYYY-MM-DD] <kind> | <summary>``. Returns WARN-grade messages so
    existing forks aren't broken on adoption; once existing entries are
    migrated, future drift will produce a single visible WARN per stray
    heading.
    """
    warnings_out: List[str] = []
    for rel, expected_kind in LOG_PREFIX_FILES.items():
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for lineno, line in enumerate(lines, start=1):
            if not line.startswith("## "):
                continue
            # Already-correct parseable heading: validate kind.
            m = LOG_PREFIX_RE.match(line)
            if m:
                kind = m.group(2)
                if kind not in LOG_PREFIX_KINDS:
                    warnings_out.append(
                        f"{rel}:{lineno} log heading has unknown kind '{kind}' "
                        f"(allowed: {', '.join(sorted(LOG_PREFIX_KINDS))})"
                    )
                continue
            # Looks like a dated heading but not parseable — flag it.
            if LOG_DATE_HEADING_RE.match(line):
                warnings_out.append(actionable(
                    what=f"{rel}:{lineno} dated heading not in parseable format: '{line.strip()}'",
                    why=f"Chronological logs use `## [YYYY-MM-DD] {expected_kind} | <summary>` so "
                        f"`grep \"^## \\[\" {rel} | tail -5` reliably extracts the recent timeline. "
                        "Inspired by Karpathy LLM-Wiki log.md convention.",
                    how=[
                        f"Rewrite as `## [YYYY-MM-DD] {expected_kind} | <summary>`",
                        f"Allowed kinds: {', '.join(sorted(LOG_PREFIX_KINDS))}",
                    ],
                ))
    return warnings_out


def check_context_profiles() -> Tuple[List[str], List[str]]:
    """v5.7 read_policy profile + context budget lint.

    Older registries did not have profiles. Treat that case as WARN for
    backwards compatibility, but enforce schema/budget once profiles exist.
    """
    errors: List[str] = []
    warnings: List[str] = []
    registry = ROOT / "memory-bank/memory-registry.yaml"
    if not registry.exists():
        return errors, warnings

    try:
        import context_budget  # type: ignore
    except Exception as exc:
        errors.append(actionable(
            what="scripts/context_budget.py is not importable",
            why="v5.7 read_policy profiles rely on the budget tool for schema and size checks.",
            how=[
                "Restore scripts/context_budget.py from the harness source",
                f"Fix the import error: {exc}",
            ],
        ))
        return errors, warnings

    text = read(registry)
    default_profile, profiles, has_profiles = context_budget.parse_registry_profiles(text)
    if not has_profiles:
        warnings.append(
            "memory-registry.yaml has no read_policy.profiles; treating as legacy full bootstrap"
        )
        return errors, warnings

    required = {"light", "standard", "full"}
    missing = sorted(required - set(profiles))
    if missing:
        errors.append(actionable(
            what="memory-registry.yaml missing read_policy profiles: " + ", ".join(missing),
            why="v5.7 requires light/standard/full so agents can keep normal tasks low-token "
                "while preserving the full governance path.",
            how=["Add read_policy.profiles.light, .standard, and .full"],
        ))

    if default_profile not in profiles:
        errors.append(actionable(
            what=f"read_policy.default_profile points to unknown profile: {default_profile}",
            why="SessionStart and budget checks need a valid default read profile.",
            how=["Set read_policy.default_profile to one of: light | standard | full"],
        ))
    elif default_profile != "light":
        warnings.append(
            f"read_policy.default_profile is '{default_profile}', expected 'light' for low-token default"
        )

    bootstrap = context_budget._parse_bootstrap_order(text)
    full_files = profiles.get("full", {}).get("files", [])
    if bootstrap and full_files and list(full_files) != bootstrap:
        errors.append(actionable(
            what="read_policy.profiles.full.files does not match legacy bootstrap_order",
            why="full profile is the compatibility path for v5.6 behavior; drift breaks old runbooks.",
            how=["Make profiles.full.files exactly match read_policy.bootstrap_order"],
        ))

    for profile in ("light", "standard"):
        if profile not in profiles:
            continue
        try:
            report = context_budget.profile_report(ROOT, profile)
        except Exception as exc:
            errors.append(f"context budget failed for profile {profile}: {exc}")
            continue
        if report.get("over_budget"):
            errors.append(actionable(
                what=(
                    f"context profile {profile} exceeds budget: "
                    f"{report.get('total_bytes')}/{report.get('budget_bytes')} bytes"
                ),
                why="Default context must stay bounded; otherwise every session pays the governance cost.",
                how=[
                    "Shorten AGENTS.md / activeContext.md / registry text",
                    "Move details into docs/agents/ and reference them only via standard/full triggers",
                    f"Re-run `python scripts/context_budget.py --profile {profile} --json`",
                ],
            ))

    return errors, warnings


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

        # v5.2 lesson-schema lint: active/Pinned lessons must declare
        # `type` (5-class MECE) and `maturity` (3-level) — both in the index
        # row AND in the section body. Drift between the two is also flagged.
        bodies = parse_lesson_bodies(lessons_text)
        draft_active = 0
        for lid, row in index.items():
            if normalize_status(row["status"]) == "archived":
                continue
            body = bodies.get(lid, {})
            row_type = row.get("type", "")
            row_mat = row.get("maturity", "")
            body_type = body.get("type", "")
            body_mat = body.get("maturity", "")

            # Missing in index row.
            if not row_type:
                errors.append(actionable(
                    what=f"lesson {lid} missing `类型` column in index",
                    why="v5.2 schema requires every active/Pinned lesson to declare a type "
                        "(model|decision|guideline|pitfall|process) so vibe-evolve can run "
                        "type-aware promotion judgments.",
                    how=[
                        f"Add `类型` cell to the {lid} row in docs/LESSONS.md `## 索引`",
                        "Pick one of: model | decision | guideline | pitfall | process",
                    ],
                ))
            elif row_type not in LESSON_TYPES:
                errors.append(actionable(
                    what=f"lesson {lid} has invalid type: '{row_type}'",
                    why="type must be one of the 5 MECE classes.",
                    how=[f"Edit {lid} row in docs/LESSONS.md to use one of: "
                         + ", ".join(sorted(LESSON_TYPES))],
                ))
            if not row_mat:
                errors.append(actionable(
                    what=f"lesson {lid} missing `成熟度` column in index",
                    why="v5.2 schema requires every active/Pinned lesson to declare a maturity "
                        "(draft|verified|proven) so vibe-evolve can run decay/promotion logic.",
                    how=[
                        f"Add `成熟度` cell to the {lid} row in docs/LESSONS.md `## 索引`",
                        "Pick one of: draft | verified | proven",
                    ],
                ))
            elif row_mat not in LESSON_MATURITIES:
                errors.append(actionable(
                    what=f"lesson {lid} has invalid maturity: '{row_mat}'",
                    why="maturity must be one of: draft | verified | proven.",
                    how=[f"Edit {lid} row in docs/LESSONS.md to use a valid maturity"],
                ))

            # Missing in body.
            if not body_type and lid in heading_set:
                warnings.append(f"lesson {lid} body missing `- 类型：` field "
                                f"(index says '{row_type or '<unset>'}')")
            elif body_type and row_type and body_type != row_type:
                errors.append(actionable(
                    what=f"lesson {lid} type drift: index='{row_type}' body='{body_type}'",
                    why="Index row and body must agree; drift means stale data leaks into "
                        "either agent bootstrap (index) or vibe-evolve judgment (body).",
                    how=[f"Reconcile {lid} type in docs/LESSONS.md (index row and `- 类型：` line)"],
                ))
            if not body_mat and lid in heading_set:
                warnings.append(f"lesson {lid} body missing `- 成熟度：` field "
                                f"(index says '{row_mat or '<unset>'}')")
            elif body_mat and row_mat and body_mat != row_mat:
                errors.append(actionable(
                    what=f"lesson {lid} maturity drift: index='{row_mat}' body='{body_mat}'",
                    why="Index row and body must agree.",
                    how=[f"Reconcile {lid} maturity in docs/LESSONS.md"],
                ))

            if row_mat == "draft":
                draft_active += 1

        # Soft cap: too many `draft` lessons in the active window dilute the
        # signal-to-noise ratio for downstream agents.
        if draft_active > 5:
            warnings.append(f"too many draft lessons in active window: {draft_active} > 5; "
                            "consider verifying or archiving the oldest drafts")

    index_path = ROOT / "evolution/lesson-index.json"
    if index_path.exists():
        try:
            data = load_json(index_path)
            lessons = data.get("lessons", []) if isinstance(data, dict) else []
            ids = [item.get("id") for item in lessons if isinstance(item, dict)]
            dupes = sorted({x for x in ids if ids.count(x) > 1 and x})
            for lid in dupes:
                errors.append(f"duplicate lesson id in lesson-index.json: {lid}")

            # v5.2: lesson-index.json must also carry type+maturity, and they
            # must match the markdown index. Out-of-sync metadata is what
            # caused L5 ghost-drift in the first place.
            md_index = parse_lessons_index(lessons_text) if lessons_text else {}
            for item in lessons:
                if not isinstance(item, dict):
                    continue
                lid = item.get("id", "")
                j_type = item.get("type", "")
                j_mat = item.get("maturity", "")
                if j_type and j_type not in LESSON_TYPES:
                    errors.append(f"lesson-index.json {lid} has invalid type: '{j_type}'")
                if j_mat and j_mat not in LESSON_MATURITIES:
                    errors.append(f"lesson-index.json {lid} has invalid maturity: '{j_mat}'")
                if lid in md_index:
                    md_type = md_index[lid].get("type", "")
                    md_mat = md_index[lid].get("maturity", "")
                    if md_type and j_type and md_type != j_type:
                        errors.append(f"lesson {lid} type drift between markdown ('{md_type}') "
                                      f"and lesson-index.json ('{j_type}')")
                    if md_mat and j_mat and md_mat != j_mat:
                        errors.append(f"lesson {lid} maturity drift between markdown ('{md_mat}') "
                                      f"and lesson-index.json ('{j_mat}')")
                    if not j_type:
                        warnings.append(f"lesson-index.json {lid} missing `type` field")
                    if not j_mat:
                        warnings.append(f"lesson-index.json {lid} missing `maturity` field")
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
        profile_errors, profile_warnings = check_context_profiles()
        errors.extend(profile_errors)
        warnings.extend(profile_warnings)

    # v5.1: L2 reference-integrity checks (paths and scripts referenced by
    # harness-governance documents must really exist on disk).
    errors.extend(check_referenced_paths())

    # v5.4: orphan-page + log-prefix hygiene (Karpathy LLM-Wiki inspired).
    warnings.extend(check_orphan_docs())
    warnings.extend(check_log_prefix())

    # v5.3: reference-tracking — scan workflow artifacts for L\d+ mentions
    # and compare against lesson-index.json. WARN when an active/Pinned
    # lesson has zero references in the active workflow corpus, or when the
    # stored `last_referenced` field is stale relative to scan results.
    index_path = ROOT / "evolution/lesson-index.json"
    if lessons_text and index_path.exists():
        try:
            data = load_json(index_path)
            items = data.get("lessons", []) if isinstance(data, dict) else []
            by_id = {it.get("id"): it for it in items if isinstance(it, dict)}
            md_index = parse_lessons_index(lessons_text)
            known_ids = set(by_id.keys()) | set(md_index.keys())
            scan = scan_lesson_refs(known_ids)
            today = _date.today().isoformat()
            for lid, info in scan.items():
                # Only flag active/Pinned lessons; archived may stay silent.
                row = md_index.get(lid, {})
                status = normalize_status(row.get("status", "")) if row else ""
                if status not in {"active", "Pinned"}:
                    continue
                stored = by_id.get(lid, {})
                stored_last = stored.get("last_referenced")
                stored_count = stored.get("reference_count")
                if int(info["count"]) == 0:  # type: ignore[arg-type]
                    maturity = stored.get("maturity") or row.get("maturity", "")
                    threshold = (LESSON_UNUSED_PROVEN_MONTHS if maturity == "proven"
                                 else LESSON_UNUSED_VERIFIED_MONTHS if maturity == "verified"
                                 else 0)
                    warnings.append(
                        f"lesson {lid} has zero references in workflow corpus "
                        f"(maturity={maturity or '?'}, threshold={threshold or 'n/a'} months); "
                        "consider archive or verify in next task"
                    )
                else:
                    if stored_last != info["last_referenced"]:
                        warnings.append(
                            f"lesson {lid} last_referenced drift: stored='{stored_last}' "
                            f"scan='{info['last_referenced']}'; run "
                            "`python scripts/check_memory_consistency.py --update-refs` to refresh"
                        )
                    if stored_count != info["count"]:
                        warnings.append(
                            f"lesson {lid} reference_count drift: stored={stored_count} "
                            f"scan={info['count']}"
                        )
        except Exception as exc:
            warnings.append(f"reference-tracking scan failed: {exc}")

    return errors, warnings


def update_refs() -> Tuple[int, int]:
    """v5.3 ``--update-refs`` writer.

    Scans for L\\d+ references and merges ``last_referenced`` /
    ``reference_count`` / ``referenced_in`` fields into
    ``evolution/lesson-index.json``. All other lesson fields (type, maturity,
    promotion_status, etc.) are preserved verbatim. Returns (updated, total).
    """
    index_path = ROOT / "evolution/lesson-index.json"
    if not index_path.exists():
        raise SystemExit("evolution/lesson-index.json not found")
    data = load_json(index_path)
    if not isinstance(data, dict):
        raise SystemExit("evolution/lesson-index.json is not an object")
    items = data.get("lessons", [])
    if not isinstance(items, list):
        raise SystemExit("evolution/lesson-index.json `lessons` must be a list")
    known_ids = {it.get("id") for it in items if isinstance(it, dict) and it.get("id")}
    scan = scan_lesson_refs(known_ids)
    updated = 0
    for it in items:
        if not isinstance(it, dict):
            continue
        lid = it.get("id")
        if not lid or lid not in scan:
            continue
        info = scan[lid]
        new_last = info["last_referenced"]
        new_count = info["count"]
        new_sources = info["sources"]
        if (it.get("last_referenced") != new_last
                or it.get("reference_count") != new_count
                or it.get("referenced_in") != new_sources):
            it["last_referenced"] = new_last
            it["reference_count"] = new_count
            it["referenced_in"] = new_sources
            updated += 1
    data["updated_at"] = _date.today().isoformat()
    index_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return updated, len(items)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="treat missing core files as errors")
    parser.add_argument("--json", action="store_true", help="print JSON result")
    parser.add_argument(
        "--update-refs",
        action="store_true",
        help="v5.3: scan workflow artifacts and write last_referenced / "
             "reference_count / referenced_in into evolution/lesson-index.json",
    )
    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="v5.6: force all errors to warnings regardless of phase "
             "(useful for discovery_only / shadow_harness mode)",
    )
    parser.add_argument(
        "--print-phase",
        action="store_true",
        help="v5.6: print project_mode + harness_phase JSON and exit 0 "
             "(used by hook scripts to decide block vs warn)",
    )
    args = parser.parse_args()

    project_mode, harness_phase = parse_registry_phase()

    if args.print_phase:
        print(json.dumps({"project_mode": project_mode, "harness_phase": harness_phase},
                         ensure_ascii=False))
        return 0

    if args.update_refs:
        updated, total = update_refs()
        msg = {"action": "update-refs", "updated": updated, "total": total,
               "path": "evolution/lesson-index.json"}
        print(json.dumps(msg, ensure_ascii=False, indent=2) if args.json
              else f"UPDATED: {updated}/{total} lessons in evolution/lesson-index.json")
        return 0

    errors, warnings = check(strict=args.strict)

    # v5.6: phase-aware degradation. discovery_only / shadow_harness 阶段
    # 把 errors 全部降级为 warnings，与 v5.1 hook_policy 语义对齐。
    # --warn-only 显式覆盖（最高优先级）。
    degrade_to_warn = args.warn_only or harness_phase in {"discovery_only", "shadow_harness"}
    if degrade_to_warn and errors:
        warnings = list(errors) + list(warnings)
        errors = []

    result = {
        "ok": not errors,
        "project_mode": project_mode,
        "harness_phase": harness_phase,
        "errors": errors,
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        phase_tag = f"[mode={project_mode} phase={harness_phase}]"
        if errors:
            print(f"FAIL: memory consistency check failed {phase_tag}")
            for e in errors:
                print(f"ERROR: {e}")
        else:
            print(f"PASS: memory consistency check passed {phase_tag}")
        for w in warnings:
            print(f"WARN: {w}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
