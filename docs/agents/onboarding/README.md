# vibe-harness Onboarding 手册集

本目录收录从 vibe-harness v5.1 引入的接入手册，配合 v5.6 项目模式与 phase 切档使用。入口选择详见 [../project-modes.md](../project-modes.md)。

## 按项目模式索引

| 模式 | 主要手册 | 入口 skill |
|---|---|---|
| `new_project` | [NEW_PROJECT_BOOTSTRAP_MANUAL.md](NEW_PROJECT_BOOTSTRAP_MANUAL.md) | [vibe-bootstrap](../../../.claude/skills/vibe-bootstrap/SKILL.md) |
| `vibe_managed_legacy` | [EXISTING_VIBE_PROJECT_RETROFIT_MANUAL.md](EXISTING_VIBE_PROJECT_RETROFIT_MANUAL.md) | [vibe-retrofit](../../../.claude/skills/vibe-retrofit/SKILL.md) |
| `unmanaged_legacy` | [UNMANAGED_LEGACY_DISCOVERY_MANUAL.md](UNMANAGED_LEGACY_DISCOVERY_MANUAL.md) | [vibe-discovery](../../../.claude/skills/vibe-discovery/SKILL.md) |

## 辅助手册

- [PROJECT_MODES_GUIDE.md](PROJECT_MODES_GUIDE.md) — 完整模式与 phase 矩阵（详版）
- [HOOKS_CODEX_CLAUDE.md](HOOKS_CODEX_CLAUDE.md) — Codex/Claude hook 配置参考
- [LEGACY_SKILLS_MIGRATION.md](LEGACY_SKILLS_MIGRATION.md) — vibe-init/vibe-alpha/vibe-omega 等旧 skill 的迁移
- [DAILY_DEVELOPMENT_RUNBOOK.md](DAILY_DEVELOPMENT_RUNBOOK.md) — 日常开发节奏
- [BEST_PRACTICES.md](BEST_PRACTICES.md) — 最佳实践速查
- [HELP.md](HELP.md) — 常见问题

## 与 v5.5 治理面的关系

这些手册作为**接入与运维参考**，不是执行契约。执行契约仍以 [../../../AGENTS.md](../../../AGENTS.md) 为单一权威，子细则仍在 [../](../) 下的 Map 文档（lifecycle / memory-model / lessons-policy / evolution-policy / safety-and-completion / hooks-and-commands）。
