# Hook、命令与并行规则

> **Layer B 摘要**
> - **何时该读**：安装新环境需配置 Codex / Claude hook、排查某个 hook 为何未触发、决定某任务能否并行、不确定某命令能否执行时需事先从 README/Makefile/scripts 发现真实命令。
> - **包含内容**：Codex/Claude hook 配置路径、最低要求、脚本接口；命令发现原则（禁止站空发明）；并行执行规则与任务内并行边界。
> - **不在此处**：hook 调用的 vibe-* skill 内部逻辑 → `.claude/skills/vibe-*/SKILL.md`；MEMORY_CHECK 阻断详细规则 → [safety-and-completion.md](safety-and-completion.md)；生命周期阶段与 hook 的对应 → [lifecycle.md](lifecycle.md)。

> 本文件展开 [AGENTS.md](../../AGENTS.md) §17 + §18 + §19。

## Hook 自动门禁

### Codex

如果当前环境支持 Codex Hooks，必须启用：

```toml
[features]
codex_hooks = true
```

推荐配置位置：

```text
~/.codex/hooks.json
<repo>/.codex/hooks.json
```

跨平台命令约束：

- Hook 命令必须使用仓库内实际脚本，并优先写成 `python "$(git rev-parse --show-toplevel)/scripts/hooks/<hook>.py"`。
- 禁止在项目级 hook 配置中硬编码 `/usr/bin/env`、Linux 绝对路径或 Windows 专属盘符；同一模板必须能在 PowerShell 与 POSIX shell 中执行。

最低要求：

- `SessionStart`：注入 memory bootstrap 提醒。
- `UserPromptSubmit`：识别非 trivial 工程任务。
- `Stop`：执行 memory consistency；失败时返回 `decision: block` 让 Codex 继续修复。

### Claude Code

推荐配置：

```text
.claude/settings.json
```

最低要求：

- `Stop` hook 调用 [scripts/hooks/memory_stop_guard.py](../../scripts/hooks/memory_stop_guard.py)。
- 失败时返回 `decision: block`，阻止任务完成。

### GitHub Copilot

Copilot **不具备 shell hook 通道**（无 SessionStart / UserPromptSubmit / Stop）。改用三层兜底：

1. **仓库级被动注入**：[.github/copilot-instructions.md](../../.github/copilot-instructions.md) 在 Copilot 每次进入本仓库时自动加载，指向 [AGENTS.md](../../AGENTS.md) 单源契约。
2. **applyTo 被动注入**：[.github/instructions/governance.instructions.md](../../.github/instructions/governance.instructions.md) 通过 `applyTo` 在治理路径（memory-bank / LESSONS / evolution / .{claude,codex,github}/skills/vibe-* / scripts/hooks 等）触达时自动加载，强制 MEMORY_CHECK / 三向同步 / 引用回填提醒。
3. **agent 自律**：AGENTS.md §11 与 vibe-* skill SKILL.md 明确 Copilot COMPLETE 前必须**主动**执行：

   ```bash
   python scripts/check_memory_consistency.py --strict
   ```

镜像策略：Copilot 优先读 `.github/skills/vibe-*`，与 `.codex/skills/vibe-*`、`.claude/skills/vibe-*` 通过 `python scripts/sync_vibe_skills.py --write` 保持字节级一致（仅治理四件套契约，`docs/` 子目录允许三端分歧）。

安装器在所有模式下都应保留现有 `.github/copilot-instructions.md`，但必须补齐缺失的 `.github/instructions/governance.instructions.md`；`scripts/check_memory_consistency.py --strict` 会检查该文件及其 `applyTo` 覆盖面。v5.7 默认安装 `--context-profile light --skill-set lean`，需要旧重治理形态时显式传 `--context-profile full --skill-set full`。

## Context Budget

Codex SessionStart 只提示默认 profile，不再要求每次通读 LESSONS。预算命令：

```bash
python scripts/context_budget.py --profile light --json
python scripts/context_budget.py --profile standard --json
```

### Hook 与 Skill 的关系

- Hook 负责兜底，不让代理忘记。
- Skill 负责告诉代理怎么检查和怎么修。
- Script 负责确定性判断。
- AGENTS 负责定义完成标准。

## 仓库命令规则

代理必须自行发现真实命令来源：

- README。
- Makefile。
- package.json。
- pyproject.toml。
- requirements。
- scripts。
- CI 配置。

禁止：

- 凭空发明构建、测试、运行命令。
- 没跑命令却写"已通过"。
- 因找不到命令就跳过验证。

若命令不明确，先查文档或脚本；仍不明确时，说明不确定性并执行最小安全检查（语法检查、导入检查、dry-run）。

## 并行执行规则

仅在以下条件全部满足时允许并行：

- 每个任务有独立 branch 或 worktree。
- 不同代理不同时编辑同一文件。
- 共享改动必须经过 REVIEW、XCHECK、GUARD 再汇合。

允许的任务内并行（v5.1 新增，参考 harness-creator）：

- 信息收集类操作（读 architecture / harness state / environment）可在同一任务内并行 spawn 子代理。
- 汇合点必须经 REVIEW，不得直接合并未验证的并行结果。

禁止：

- 对同一关键模块静默并行修改。
- 存在跨任务依赖却不显式说明。
- 未验证直接合并并行结果。
