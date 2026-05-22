# GitHub Copilot 仓库级指令

> 本文件是 Copilot 在本仓库的**入口指针**，权威执行契约在 [AGENTS.md](../AGENTS.md)。

## 1. 必读：AGENTS.md

任何改动前先读 [AGENTS.md](../AGENTS.md)（v5.5+），它定义：

- 标准生命周期 `INIT → MEMORY_BOOTSTRAP → PLAN → ALPHA → REVIEW → EXEC → XCHECK → GUARD → CHANGELOG → LESSONS → EVOLVE → MEMORY_CHECK → COMPLETE`
- 冲突优先级：`用户当前指令 > 系统/开发者指令 > 项目 AGENTS > 全局 AGENTS > memory-bank > lessons`
- MEMORY_BOOTSTRAP 必读清单（memory-bank、LESSONS、lesson-index）
- vibe-* 治理四件套（memory-check / guard / xcheck / evolve）

Copilot 优先读 `.github/skills/vibe-*`，但三向镜像（`.claude/skills` / `.codex/skills` / `.github/skills`）保持字节一致，跨代理行为收敛。

## 2. Copilot 专属约束

### 2.1 无 shell hook → 主动自律

Copilot **没有 SessionStart / Stop hook 通道**。COMPLETE 前必须**主动**执行：

```bash
python scripts/check_memory_consistency.py --strict
```

失败不得 COMPLETE。这与 Codex / Claude 的自动门禁结果对齐。

### 2.2 applyTo 被动注入

治理面（`memory-bank/`、`docs/LESSONS*.md`、`docs/agents/**`、`evolution/**`、`AGENTS.md`、`.{claude,codex,github}/skills/vibe-*/**`、`scripts/hooks/**`、`scripts/sync_vibe_skills.py`）的改动会通过 [.github/instructions/governance.instructions.md](instructions/governance.instructions.md) 的 `applyTo` 自动注入治理提醒，强化 MEMORY_CHECK 自律。

### 2.3 memory 边界

- `/memories/`（user-level）：跨工作区个人偏好，允许。
- `/memories/session/`：仅本会话临时笔记，允许。
- `/memories/repo/`：**禁止用于仓库事实**。仓库事实统一进 [memory-bank/](../memory-bank/)；如需写入，先回 AGENTS.md 评估。

### 2.4 三向同步

任何对 `.claude/skills/vibe-*`（治理四件套契约）的改动后，必须：

```bash
python scripts/sync_vibe_skills.py --write
python scripts/sync_vibe_skills.py --check
```

让 `.codex/skills/vibe-*` 与 `.github/skills/vibe-*` 保持字节级一致。

## 3. 通用编码规范（与 AGENTS.md 一致）

- **测试**：TDD；修 bug 先写失败测试（Prove-It）；测试层级取最低能覆盖的（单元 > 集成 > 端到端）。
- **代码质量**：五维度评审（正确性 / 可读性 / 架构 / 安全 / 性能）；PR 必过 lint、类型、测试、构建；禁止提交密钥。
- **实现**：小步快走，每增量「实现 → 测试 → 验证 → 提交」，不混合格式化与行为修改。
- **边界**：提交前跑测试、验证输入；先询问后操作的项 = schema 变更 / 新增依赖；禁止跳过验证、删失败测试、提交密钥。
