# SYSTEM CONTRACT (VibeCoding)

> Version: v1.0
> Date: 2026-02-02

This repository is governed by the **VibeCoding** protocol.

## Core principles (hard)
1. **Plan-first**: No production code without an approved plan.
2. **Context-as-code**: `memory-bank/` is the source of truth; keep it in sync.
3. **Glue-first**: Prefer integration/compose over reinventing.
4. **Maintainability gates**: small modules, explicit errors/logging, tests, no hard-coded secrets.
5. **Scope control**: Any scope change must update PRD/Plan before execution.

## Gates (workflow)
- Gate A: Clarify (>=9 key questions unless AC already explicit)
- Gate B: Plan-only (steps include verification)
- Gate C: Confirm (convert plan into executable task list)
- Gate D: Execute (TDD, modular, observable, fail-visible)
- Gate E: Omega audit (optional but recommended)
- Gate F: Git submit (atomic commits + checklist + progress update)
