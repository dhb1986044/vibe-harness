---
name: vibe-discovery
description: Read-only discovery for unmanaged legacy projects without AGENTS or memory. Use before coding in human-created historical projects. Sets harness_phase=discovery_only.
---

# vibe-discovery

Use when the repository has **no AGENTS.md, no memory-bank, no LESSONS**, and was built entirely by humans without any harness.

不适用：

- 空项目 → 用 `vibe-bootstrap`。
- 已有部分 harness 痕迹的项目 → 用 `vibe-retrofit`。

## 硬性约束

- **只读优先**：禁止修改业务代码。
- **不删除、不重命名**任何历史文件。
- **不启用 blocking hooks**：保持 `harness_phase: discovery_only`。
- 所有生成物以 `*.draft.md` / `PROJECT_DISCOVERY_REPORT.md` 形式落盘，须人工确认后才能升级。

## 执行步骤

1. **运行只读侦察**：

   ```bash
   python scripts/discover_project.py --write
   ```

   产出：
   - `PROJECT_DISCOVERY_REPORT.md`（命令清单、文件树、未知项）
   - `memory-bank/architecture.draft.md`
   - `memory-bank/tech-stack.draft.md`
   - `AGENTS.draft.md`（如缺失）

2. **声明项目模式**：创建最小 `memory-bank/memory-registry.yaml`：
   - `project_mode: unmanaged_legacy`
   - `harness_phase: discovery_only`
3. **人工确认**：
   - 标记 `unknowns` 中每一项的真实情况。
   - 转正 `*.draft.md`（去掉 `.draft` 后缀，写入 registry `core_files`）。
4. **升级到 shadow_harness**：当 memory-bank 初稿完成并经人工确认后，切到 `vibe-retrofit` 流程。

## 验收

- `python scripts/check_memory_consistency.py --warn-only` 输出 warnings 但不 block。
- 生成的所有文件都是 `*.draft.md` 或 `PROJECT_DISCOVERY_REPORT.md`，未触碰业务代码。

## 自动化

```bash
python scripts/install_vibe_harness.py --target /path/to/repo --mode discovery --dry-run
python scripts/install_vibe_harness.py --target /path/to/repo --mode discovery
```

参考：[docs/agents/project-modes.md](../../../docs/agents/project-modes.md)
