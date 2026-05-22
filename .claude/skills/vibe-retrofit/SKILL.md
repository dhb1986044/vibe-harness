---
name: vibe-retrofit
description: Upgrade an existing vibe-managed project to v5.6 without breaking old skills or memory. Use when AGENTS.md / memory-bank / LESSONS already exist.
---

# vibe-retrofit

Use when the project already has AGENTS.md, memory-bank, LESSONS, or old `vibe-init/vibe-alpha/vibe-omega` skills.

不适用：

- 空项目 → 用 `vibe-bootstrap`。
- 纯人工历史项目 → 用 `vibe-discovery`。

## 执行步骤（渐进升级，禁止一次性硬切）

1. **盘点现有 harness**：
   - 列出已有 AGENTS.md / memory-bank/*.md / LESSONS*.md / 旧 vibe-* skill。
   - 识别旧 skill：`vibe-init` / `vibe-alpha` / `vibe-omega` 等不再推荐的入口。
2. **声明项目模式**：在 `memory-bank/memory-registry.yaml` 设置：
   - `project_mode: vibe_managed_legacy`
   - `harness_phase: shadow_harness`（**起步阶段**，不要直接 managed）
3. **生成/补全 registry**：
   - 补齐 `core_files` / `read_policy.bootstrap_order` / `governance_paths`。
   - 补齐 `lessons_policy` 的 v5.2 schema（type / maturity）。
4. **legacy 适配**：将 `vibe-init / vibe-alpha / vibe-omega` 移入：
   - `.claude/skills/_legacy/`
   - `.codex/skills/_legacy/`
   - 不直接删除；观察 1~2 周无触发后再归档到 `archive/legacy-skills/`。
5. **安装 v5.6 治理四件套**：vibe-memory-check / vibe-guard / vibe-xcheck / vibe-evolve（用 `python scripts/sync_vibe_skills.py --write`）。
6. **hook 切档**：先 `shadow_harness`（warn-only） → `soft_gate`（仅治理面 block） → `managed_harness`（全量 block）。每次切档前确认误报率 ≤10%。
7. **LESSONS 迁移**：把现有 lesson 补齐 type / maturity 字段；用 `python scripts/check_memory_consistency.py --update-refs` 更新引用追踪。

## 切档判据

- `shadow_harness` → `soft_gate`：连续 5 个任务无误报，团队评审通过，AI_CHANGELOG 记录。
- `soft_gate` → `managed_harness`：业务面也无误报，CI 稳定 ≥1 周。

## 验收

- `python scripts/check_memory_consistency.py --strict` 在当前 phase 下符合预期（discovery/shadow 期允许 warn）。
- `python scripts/sync_vibe_skills.py --check` 通过。
- 旧 skill 已迁入 `_legacy/`。

## 自动化

```bash
python scripts/install_vibe_harness.py --target /path/to/repo --mode retrofit --dry-run
python scripts/install_vibe_harness.py --target /path/to/repo --mode retrofit
```

参考：[docs/agents/project-modes.md](../../../docs/agents/project-modes.md)
