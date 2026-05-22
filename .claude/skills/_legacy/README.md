# _legacy/ 旧 skill 适配通道

本目录用于存放被 v5.6 弃用但仍可能在历史项目中触发的旧 skill 适配壳（如 `vibe-init` / `vibe-alpha` / `vibe-omega`）。

**本仓库自身不需要 legacy skill**（直接生于 v5.x），因此此目录在主仓保持为空，仅作为 [vibe-retrofit](../vibe-retrofit/SKILL.md) 流程的占位说明。

## 在目标项目中的使用

当 `vibe-retrofit` 接入既有项目时，会把目标项目中的 `vibe-init` / `vibe-alpha` / `vibe-omega` 等旧 skill 平移到目标项目的 `.claude/skills/_legacy/` 与 `.codex/skills/_legacy/`，并在 1~2 周观察期后归档到 `archive/legacy-skills/`。

详见 [docs/agents/onboarding/LEGACY_SKILLS_MIGRATION.md](../../../docs/agents/onboarding/LEGACY_SKILLS_MIGRATION.md)。
