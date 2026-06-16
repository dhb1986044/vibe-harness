<!-- markdownlint-disable MD041 -->
# AGENTS.md v5.7 - Agent Harness 执行契约

仓库级行为契约，不是 README 或知识库。细节按需读 [docs/agents/](docs/agents/)，历史版见 [AGENTS.legacy.md](AGENTS.legacy.md)。

## 0. 优先级

冲突优先级：

```text
用户当前指令 > 系统/开发者指令 > 项目 AGENTS > 目录级 AGENTS.override.md > 全局 AGENTS > memory-bank > lessons/archive
```

总原则：`稳定性 > 可回滚性 > 可维护性 > 可解释性 > 性能 > 优雅性`。先读后改；命令来自真实文件；不伪造验证。

## 1. Context Profile

读取策略由 [memory-bank/memory-registry.yaml](memory-bank/memory-registry.yaml) 的 `read_policy` 声明。

| Profile | 默认用途 | 必读 |
|---|---|---|
| `light` | 默认启动、简单问答、低风险定位 | 本文件 + registry + `activeContext.md` |
| `standard` | 普通代码/配置任务 | light + 架构/命令/最近进展/少量 lessons |
| `full` | 治理路径、高风险、失败复盘 | v5.6 完整 bootstrap |

扩展规则：

- 需要真实命令时读 `memory-bank/tech-stack.md` 或 README/scripts/CI。
- 触达 hook、安装器、checker、skills、memory、LESSONS、evolution 或非平凡治理路径时用 `full`；小型 docs-only 按 `L1` 处理。
- 返工、同类失败、风险不清或破坏性操作时用 `full` 并进入 GUARD。
- 预算检查：`python scripts/context_budget.py --profile light --json`。

风险分级：`L0` typo/单文件文案用 `light` 且无需 skill；`L1` docs-only 用 `light`+命中文档，治理收尾跑 memory check；`L2` 单侧 runtime/配置/测试用 `standard` + 局部 XCHECK；`L3` contract/schema/cross-stack/high-risk 用 `full` + 完整闭环。

## 2. 项目模式

接入项目前先识别模式，详见 [project-modes.md](docs/agents/project-modes.md)。

| 模式 | 适用场景 | 入口 skill | 初始 phase |
|---|---|---|---|
| `new_project` | 空仓库 | `vibe-bootstrap` | `managed_harness` |
| `vibe_managed_legacy` | 已有 harness 痕迹 | `vibe-retrofit` | `shadow_harness` -> `soft_gate` -> `managed_harness` |
| `unmanaged_legacy` | 人工历史项目 | `vibe-discovery` | `discovery_only` |

`harness_phase` 控制 hook：`discovery_only`、`shadow_harness` 只 warn；`soft_gate` 只阻断治理面；`managed_harness` 任失败均阻断。

## 3. 生命周期

标准闭环：

```text
INIT -> MEMORY_BOOTSTRAP -> PLAN -> EXEC -> XCHECK -> GUARD -> CHANGELOG -> LESSONS -> EVOLVE -> MEMORY_CHECK -> COMPLETE
```

执行约束：

- 普通任务按最小必要阶段执行，不能为了完整感扩大范围。
- EXEC 后必须 XCHECK：正向、边界、负面、回归、受影响模块 sanity。
- 以下情况必须 GUARD：核心重写、大规模删除/重构、schema/API 破坏、依赖/构建链变化、安全/权限/token/出网变化、发布入口或安装器变化、测试不足但行为改变。
- 仓库状态发生非平凡变化时更新 [docs/AI_CHANGELOG.md](docs/AI_CHANGELOG.md)。
- 只有失败、返工、新风险、可复用流程规则才更新 [docs/LESSONS.md](docs/LESSONS.md) 并评估 EVOLVE。

阶段细则见 [lifecycle.md](docs/agents/lifecycle.md)、[safety-and-completion.md](docs/agents/safety-and-completion.md)。

## 4. Memory 与 Lessons

- 仓库事实进 [memory-bank/](memory-bank/)，经验进 [docs/LESSONS.md](docs/LESSONS.md)，能力固化进 skills/hooks/templates。
- 默认不通读 `docs/LESSONS_ARCHIVE.md`。
- LESSONS 默认只读 Active Summary、Pinned 和 profile 指定的最近条目；命中标签/关键词/模块/同类失败时再展开。
- 引用 lesson 时用裸编号，如 `L12`，便于 `python scripts/check_memory_consistency.py --update-refs` 回填。

## 5. 完成门禁

触达以下任一路径时，COMPLETE 前必须运行：

```bash
python scripts/check_memory_consistency.py --strict
```

治理路径：`AGENTS.md`、`docs/agents/**`、`memory-bank/**`、`docs/LESSONS*.md`、`docs/AI_CHANGELOG.md`、`evolution/**`、`.*/skills/vibe-*/**`、`.github/instructions/**`、`.github/copilot-instructions.md`、`scripts/hooks/**`、`scripts/sync_vibe_skills.py`、`scripts/check_memory_consistency.py`、`scripts/context_budget.py`、`scripts/evolve_lessons.py`。

失败不得 COMPLETE。Copilot 没有 shell Stop hook，必须主动执行该命令；`/memories/repo/` 禁止用于仓库事实。

## 6. Skill 路由

只触发本仓库 `.codex/.claude/.github` 下的 `vibe-*` skill。默认 lean 和日常路由只推荐核心 8 个；其它 Codex skill 仅明确场景或 `--skill-set full` 使用。

| 场景 | 默认 skill |
|---|---|
| 初始化/接入 | `vibe-bootstrap` / `vibe-retrofit` / `vibe-discovery` |
| 执行 | `vibe-exec` |
| 验证/风险 | `vibe-xcheck` / `vibe-guard` |
| 晋升/完成 | `vibe-evolve` / `vibe-memory-check` |

可选高级：`vibe-plan/context/changelog/lessons/debug/review/alpha/init/knowledge/omega/pipeline/git`；源码存在不等于默认触发。

治理四件套 `vibe-memory-check / vibe-guard / vibe-xcheck / vibe-evolve` 以 `.claude/skills/` 为单源，`.codex/skills/` 与 `.github/skills/` 镜像；`docs/` 子目录允许端侧分歧。同步命令：

```bash
python scripts/sync_vibe_skills.py --write
python scripts/sync_vibe_skills.py --check
```

## 7. 导航

[memory-model.md](docs/agents/memory-model.md) | [lifecycle.md](docs/agents/lifecycle.md) | [lessons-policy.md](docs/agents/lessons-policy.md) | [evolution-policy.md](docs/agents/evolution-policy.md) | [safety-and-completion.md](docs/agents/safety-and-completion.md) | [hooks-and-commands.md](docs/agents/hooks-and-commands.md)
