---
name: vibe-bootstrap
description: Initialize a new project with vibe-harness v5.6. Use only for new or empty projects. Sets project_mode=new_project, harness_phase=managed_harness.
---

# vibe-bootstrap

Use when a project is new or intentionally being initialized from scratch (no existing AGENTS.md, no memory-bank, no LESSONS).

不适用：

- 已有 AGENTS.md / memory-bank / LESSONS 的项目 → 用 `vibe-retrofit`。
- 纯人工历史项目（无任何 harness 痕迹）→ 用 `vibe-discovery`。

## 执行步骤

1. **声明项目模式**：创建 `memory-bank/memory-registry.yaml`，设置：
   - `project_mode: new_project`
   - `harness_phase: managed_harness`
2. **生成治理面骨架**：
   - `AGENTS.md`（Map 结构，链接到 `docs/agents/*.md`）
   - `memory-bank/`：activeContext.md / progress.md / architecture.md / tech-stack.md / prd.md
   - `docs/`：LESSONS.md / LESSONS_RULES.md / LESSONS_ARCHIVE.md / AI_CHANGELOG.md
   - `evolution/`：lesson-index.json / promotion-log.md
3. **安装治理四件套 skill**：vibe-memory-check / vibe-guard / vibe-xcheck / vibe-evolve（三向镜像同步：`python scripts/sync_vibe_skills.py --write`）。
4. **配置 hooks**：
   - Codex：`.codex/hooks.json`（Stop / SessionStart / UserPromptSubmit / PreToolUse）
   - Claude：`.claude/settings.json` 的 Stop hook
   - Copilot：`.github/copilot-instructions.md` + `.github/instructions/governance.instructions.md`
5. **首次 MEMORY_CHECK**：`python scripts/check_memory_consistency.py --strict` 必须 PASS。

## 验收

- `python scripts/check_memory_consistency.py --print-phase` 返回 `new_project / managed_harness`。
- `python scripts/sync_vibe_skills.py --check` 通过。
- `docs/AI_CHANGELOG.md` 记录 bootstrap 事件。

## 自动化

```bash
python scripts/install_vibe_harness.py --target /path/to/repo --mode bootstrap --dry-run
python scripts/install_vibe_harness.py --target /path/to/repo --mode bootstrap
```

完成 bootstrap 后，所有后续任务回归标准生命周期（INIT → MEMORY_BOOTSTRAP → ... → COMPLETE）。

参考：[docs/agents/project-modes.md](../../../docs/agents/project-modes.md)
