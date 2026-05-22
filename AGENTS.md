<!-- markdownlint-disable MD041 -->
# AGENTS.md v5.1 — Agent Harness 执行契约（Map）

本文件是本仓库所有编码代理的仓库级执行契约。适用于 Codex、Claude Code、Gemini CLI、GitHub Copilot、OpenClaw 等代理。

> **AGENTS.md is a Map, Not a Manual.** 本文件只列骨架与导航；细节在 [docs/agents/](docs/agents/)。完整旧版保留为 [AGENTS.legacy.md](AGENTS.legacy.md)，用于回滚对比。

## 0. 定位

AGENTS.md 不是 README，也不是知识库。它是代理改变仓库状态前必须遵守的"行为契约"。

代理必须同时满足：(1) 知道目标与边界；(2) 知道仓库真实事实；(3) 知道历史经验；(4) 能证明改动正确；(5) 能评估风险与回滚；(6) 能把经验沉淀为下一次能力。

闭环：

```text
MEMORY_BOOTSTRAP -> PLAN -> EXEC -> XCHECK -> GUARD -> CHANGELOG -> LESSONS -> EVOLVE -> MEMORY_CHECK -> COMPLETE
```

## 1. 分层与冲突优先级

- **全局 AGENTS**：`~/.codex/AGENTS.md`、`~/.claude/CLAUDE.md`、`~/.gemini/GEMINI.md`，只写跨项目稳定原则。
- **项目 AGENTS**：本文件，只写本仓库执行契约。事实进 [memory-bank/](memory-bank/)，经验进 [docs/LESSONS.md](docs/LESSONS.md)。

冲突优先级（高 → 低）：

```text
用户当前指令 > 系统/开发者指令 > 项目 AGENTS > 目录级 AGENTS.override.md > 全局 AGENTS > memory-bank > lessons/archive
```

### 1.1 三类项目模式（v5.6）

接入 vibe-harness 前必须先识别项目模式，决定入口 skill 与初始 harness 阶段：

| 模式 | 适用场景 | 入口 skill | 初始 phase |
|---|---|---|---|
| `new_project` | 空仓库 / 刚开始规划 | [vibe-bootstrap](.claude/skills/vibe-bootstrap/SKILL.md) | `managed_harness` |
| `vibe_managed_legacy` | 已有 AGENTS / memory / LESSONS / 旧 vibe-* | [vibe-retrofit](.claude/skills/vibe-retrofit/SKILL.md) | `shadow_harness` → `soft_gate` → `managed_harness` |
| `unmanaged_legacy` | 纯人工历史项目，无 harness 痕迹 | [vibe-discovery](.claude/skills/vibe-discovery/SKILL.md) | `discovery_only` → ... |

`harness_phase` 四档（在 [memory-bank/memory-registry.yaml](memory-bank/memory-registry.yaml) 声明，hook 据此决定 block / warn）：

- `discovery_only`：只读侦察，永不 block
- `shadow_harness`：影子运行，仅 warn
- `soft_gate`：仅治理面失败 block
- `managed_harness`：任何 memory check 失败均 block

本仓库自身为 `vibe_managed_legacy` + `managed_harness`。详见 [docs/agents/project-modes.md](docs/agents/project-modes.md)。

## 2. 总原则

优先级：`稳定性 > 可回滚性 > 可维护性 > 可解释性 > 性能 > 优雅性`

执行原则：

- 先思考再编码；简单优先；外科手术式改动；目标驱动。
- 尊重真实架构；先读后改；不发明命令；不伪造验证。

## 3. Memory 模型

四层 memory：L1 会话态 → L2 项目态 → L3 经验态 → L4 能力态。L3 须通过 EVOLVE 晋升 L4，避免无限堆积。详见 [docs/agents/memory-model.md](docs/agents/memory-model.md)。

## 4. 标准生命周期

```text
INIT -> MEMORY_BOOTSTRAP -> PLAN -> ALPHA -> REVIEW -> EXEC -> XCHECK -> GUARD -> CHANGELOG -> LESSONS -> EVOLVE -> MEMORY_CHECK -> COMPLETE
```

每个状态的目标、产物、失败回退见 [docs/agents/lifecycle.md](docs/agents/lifecycle.md)。

## 5. MEMORY_BOOTSTRAP 必读清单

任务开始前，按顺序读取：

1. `AGENTS.md`（本文件）
2. `memory-bank/memory-registry.yaml`
3. `memory-bank/activeContext.md`
4. `memory-bank/progress.md`
5. `memory-bank/architecture.md`
6. `memory-bank/tech-stack.md`
7. `docs/LESSONS.md`（Active Summary + Pinned + 最近 5~10 条）
8. `evolution/lesson-index.json`

按需读取 [docs/agents/](docs/agents/) 下细则文档。详见 [memory-model.md](docs/agents/memory-model.md)。

## 6. XCHECK 触发清单

EXEC 后必须覆盖：正向最小可用、边界、负面、回归、受影响模块 sanity、性能 sanity（如适用）。失败回 REVIEW/EXEC，不得跳过。详见 [lifecycle.md](docs/agents/lifecycle.md)。

## 7. GUARD 触发清单

以下情况必须 GUARD：

- 核心逻辑重写 / 大规模删除或重构
- Schema 变更 / API 破坏性变更
- 工具链、构建链、依赖升级
- 安全、权限、token、密钥、出网配置变化
- 发布仓 / 插件 manifest / marketplace / 安装入口变化
- 测试覆盖不足但行为已变化

输出：风险等级（低/中/高）+ 回滚方案 + 关键假设 + 残余风险。无回滚的高风险改动不得完成。

## 8. CHANGELOG / LESSONS / EVOLVE

- 仓库状态变化 → 更新 [docs/AI_CHANGELOG.md](docs/AI_CHANGELOG.md)
- 失败/返工/新风险 → 更新 [docs/LESSONS.md](docs/LESSONS.md)（治理细则见 [lessons-policy.md](docs/agents/lessons-policy.md)）
- 是否晋升 L4 → 见 [evolution-policy.md](docs/agents/evolution-policy.md)；执行 `python scripts/evolve_lessons.py --write`

## 9. MEMORY_CHECK

涉及 `AGENTS.md`、`docs/agents/**`、`memory-bank/**`、`docs/LESSONS*.md`、`docs/AI_CHANGELOG.md`、`evolution/**`、`.codex/skills/vibe-*/**`、`.claude/skills/vibe-*/**`、`.github/skills/vibe-*/**`、`.github/instructions/**`、`.github/copilot-instructions.md`、`scripts/hooks/**`、`scripts/sync_vibe_skills.py` 变更时，必须执行：

```bash
python scripts/check_memory_consistency.py --strict
```

失败不得 COMPLETE。详见 [safety-and-completion.md](docs/agents/safety-and-completion.md)。

## 10. Hook、命令、并行

- Codex/Claude hook 配置与最低要求：见 [hooks-and-commands.md](docs/agents/hooks-and-commands.md)。
- Copilot **没有 shell hook 通道**，依赖三层兜底：(1) `.github/copilot-instructions.md` 仓库级被动注入（指向 AGENTS.md）；(2) `.github/instructions/*.instructions.md` 通过 `applyTo` 在治理面被动注入；(3) AGENTS.md / vibe-* skill 的 agent 自律。Copilot 不享受 SessionStart/Stop 兜底，必须在 COMPLETE 前**主动**执行 `python scripts/check_memory_consistency.py --strict`。
- 命令必须来自仓库真实文件（README/Makefile/scripts/...），禁止凭空发明。
- 并行执行规则（含任务内并行）：见 [hooks-and-commands.md](docs/agents/hooks-and-commands.md)。

## 11. 安全与完成标准

- 不得提交真实 token、密钥、cookie。
- 删除/重命名/迁移前评估回滚。
- 完成清单：用户成功标准 + XCHECK + GUARD + CHANGELOG + LESSONS + EVOLVE + memory-bank 同步 + MEMORY_CHECK。
- Copilot 注意：无 Stop hook，COMPLETE 前必须**主动**调用 `python scripts/check_memory_consistency.py --strict`；`/memories/repo/` **禁止用于仓库事实**（仓库事实统一进 `memory-bank/`），`/memories/session/` 仅放本会话临时笔记。

详见 [safety-and-completion.md](docs/agents/safety-and-completion.md)。

## 12. vibe-* Skill 索引

**触发面**：本仓库代理只能触发 `.codex/skills/vibe-*`、`.claude/skills/vibe-*` 与 `.github/skills/vibe-*` 中的 skill，禁止依赖外部通用 skill。Copilot 优先读 `.github/skills/vibe-*`，但因三向镜像字节一致，跨代理行为收敛。

**单源策略（仅治理四件套契约）**：[vibe-memory-check / vibe-guard / vibe-xcheck / vibe-evolve](.claude/skills/) 的契约文件（`SKILL.md` + 非 `docs/` 顶层文件）以 `.claude/skills/` 为单源，`.codex/skills/` 与 `.github/skills/` 必须字节级一致；各 skill 的 `docs/` 子目录允许三端分歧（例如 `.codex` 端从 harness-creator 引入富文档），由 `python scripts/sync_vibe_skills.py --write` 维护。其余 codex 独有 skill（如 vibe-init、vibe-plan、vibe-alpha、vibe-omega、vibe-pipeline、vibe-changelog、vibe-lessons、vibe-review、vibe-debug、vibe-knowledge、vibe-context、vibe-git）**不**纳入镜像约束。

**治理四件套**：

| Skill | 何时使用 |
|---|---|
| [vibe-memory-check](.claude/skills/vibe-memory-check/SKILL.md) | AGENTS/memory-bank/LESSONS/evolution 变更前 COMPLETE |
| [vibe-guard](.claude/skills/vibe-guard/SKILL.md) | 高风险改动前评估 |
| [vibe-xcheck](.claude/skills/vibe-xcheck/SKILL.md) | EXEC 后验证 |
| [vibe-evolve](.claude/skills/vibe-evolve/SKILL.md) | LESSONS 是否需晋升 |

**入口 skill（v5.6，按项目模式触发一次，不纳入三向镜像）**：

| Skill | 何时使用 |
|---|---|
| [vibe-bootstrap](.claude/skills/vibe-bootstrap/SKILL.md) | `new_project` — 空仓库初始化 |
| [vibe-retrofit](.claude/skills/vibe-retrofit/SKILL.md) | `vibe_managed_legacy` — 已有 harness 升级到 v5.6 |
| [vibe-discovery](.claude/skills/vibe-discovery/SKILL.md) | `unmanaged_legacy` — 历史项目只读侦察 |
| [vibe-exec](.claude/skills/vibe-exec/SKILL.md) | 可选 — 包装 EXEC 阶段的最小可回滚改动 |

入口 skill 分别维护于 `.claude/skills/` 与 `.codex/skills/`，**不**经 `sync_vibe_skills.py` 镜像，允许两端独立演进。Copilot 通过 §1.1 与 [docs/agents/project-modes.md](docs/agents/project-modes.md) 跳转，不在 `.github/skills/` 复制。

**功能 skill 与生命周期映射**：见 [docs/agents/memory-model.md](docs/agents/memory-model.md) "触发矩阵"章节。

---

**导航 Map**：[lifecycle.md](docs/agents/lifecycle.md) ｜ [memory-model.md](docs/agents/memory-model.md) ｜ [lessons-policy.md](docs/agents/lessons-policy.md) ｜ [evolution-policy.md](docs/agents/evolution-policy.md) ｜ [safety-and-completion.md](docs/agents/safety-and-completion.md) ｜ [hooks-and-commands.md](docs/agents/hooks-and-commands.md)
