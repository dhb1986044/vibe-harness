# Memory 模型

> **Layer B 摘要**
> - **何时该读**：MEMORY_BOOTSTRAP 阶段要决定读什么、需要区分 L1~L4 哪一层路径、设计新 skill / hook 时需参考触发矩阵、不确定某件事实应入 memory-bank 还是 LESSONS 。
> - **包含内容**：L1 会话态 / L2 项目态 / L3 经验态 / L4 能力态四层 memory 的位置、所有者与生命周期；vibe-* 治理四件套与功能 skill 的触发矩阵；read_policy profile。
> - **不在此处**：LESSONS 写入 / 归档 / 引用追踪规则 → [lessons-policy.md](lessons-policy.md) + [../LESSONS_RULES.md](../LESSONS_RULES.md)；L4 晋升判定 → [evolution-policy.md](evolution-policy.md)；MEMORY_CHECK 如何阻断 COMPLETE → [safety-and-completion.md](safety-and-completion.md)。

> 本文件展开 [AGENTS.md](../../AGENTS.md) §3 + §6。

## 四层 Memory

```text
L1 会话态 memory：当前任务上下文，主要是 memory-bank/activeContext.md
L2 项目态 memory：架构、技术栈、命令、进度，主要是 memory-bank/*.md
L3 经验态 memory：失败模式、修复策略、复用模式，主要是 docs/LESSONS.md
L4 能力态 memory：已固化为 skills、guards、xchecks、templates 的能力
```

L3 不应无限堆积。高频、严重、可复用、可验证的 lessons 必须通过 EVOLVE 晋升为 L4。详见 [evolution-policy.md](evolution-policy.md)。

## MEMORY_BOOTSTRAP 读取 Profile

任务开始先读 [AGENTS.md](../../AGENTS.md) 与 [memory-bank/memory-registry.yaml](../../memory-bank/memory-registry.yaml)，再按 `read_policy.default_profile` 选择读取范围。默认是 `light`。

| Profile | 读取范围 | 触发条件 |
|---|---|---|
| `light` | AGENTS、registry、[activeContext.md](../../memory-bank/activeContext.md) | 默认启动、简单问答、低风险定位 |
| `standard` | light + architecture/tech-stack + progress 最新条目 + LESSONS 摘要/Pinned/最近 3 条 | 普通代码、配置、构建/测试命令、模块边界问题 |
| `full` | v5.6 完整 bootstrap_order | 非平凡治理路径、高风险、失败复盘、LESSONS/EVOLVE/memory/schema/hook 变更 |

任务风险到 profile 的默认映射：

| Level | 场景 | 默认读取 | 说明 |
|---|---|---|---|
| `L0` | typo、单文件文案、无行为变更 | `light` | 不触发完整 lifecycle，不默认读 LESSONS。 |
| `L1` | docs-only / 小型治理修正 | `light` + 命中文档；治理面变更收尾跑 memory check | 只有命中治理路径或风险不清时升 `full`。 |
| `L2` | 前端、后端、脚本或配置单侧变更 | `standard` | 读取真实命令来源并做局部 XCHECK。 |
| `L3` | contract/schema/cross-stack/high-risk | `full` | 执行完整治理闭环和 GUARD。 |

预算检查：

```bash
python scripts/context_budget.py --profile light --json
python scripts/context_budget.py --profile standard --json
```

## 读取策略

- 默认不通读 `docs/LESSONS_ARCHIVE.md`。
- 默认不通读完整 `docs/LESSONS.md`，只取 profile 声明的摘要/条目。
- 命中标签、关键词、模块、同类失败时，再按需读取 archive 或完整 lesson。
- 若 `memory-registry.yaml` 缺失，任务仍可继续，但必须在 CHANGELOG/LESSONS 中记录 memory harness 未完整。

## memory-bank 初始化清单（植入新/旧项目时使用）

5 个核心事实文件默认为占位骨架，**不会**被一致性检查脚本强制填充，但是代理 bootstrap 质量的关键输入。建议按以下顺序填写：

| 顺序 | 文件 | 什么时候写 | 必填字段 |
|---|---|---|---|
| 1 | [prd.md](../../memory-bank/prd.md) | 项目启动 / 大型需求变更 | 产品目标、目标用户、范围、成功指标 |
| 2 | [tech-stack.md](../../memory-bank/tech-stack.md) | 项目启动 / 依赖重大变更 | 语言 + 包管理器 + **真实命令**（构建/测试/Lint） |
| 3 | [architecture.md](../../memory-bank/architecture.md) | 项目启动 / 架构变动 / 新增模块 | 顶层设计、模块边界、不变量与架构红线 |
| 4 | [progress.md](../../memory-bank/progress.md) | 每次任务 EXEC 后 | 时间戳、已完成、进行中、阻塞、下一步 |
| 5 | [activeContext.md](../../memory-bank/activeContext.md) | 每轮任务 INIT/PLAN 阶段 | 当前焦点、任务范围、关键假设、下一动作 |

原则：

- **事实不是知识库**：只记录稳定事实与决策，详细设计文档走 `docs/`。
- **真实命令优先从 README/Makefile/package.json/pyproject.toml 提取**，禁止凭空生成（L1 教训）。
- **prd.md / architecture.md / tech-stack.md 是低频写文件**；progress.md / activeContext.md 是高频写文件。
- 填写后运行 `python scripts/check_memory_consistency.py --strict` 验证。

## 触发矩阵（场景 → vibe-* Skill → 文件）

> 本仓库代理**只能触发** `.codex/skills/vibe-*`、`.claude/skills/vibe-*` 与 `.github/skills/vibe-*` 中的 skill。禁止使用通用 skill 名（如 spec-driven-development、planning-and-task-breakdown 等）作为触发器。
>
> 默认 lean 安装只暴露 8 个 skill：治理四件套（`vibe-memory-check / vibe-guard / vibe-xcheck / vibe-evolve`）+ 接入/执行最小集（`vibe-bootstrap / vibe-retrofit / vibe-discovery / vibe-exec`）。其它 `.codex/skills/vibe-*` 是 optional / advanced / source-only，只有明确场景或 `--skill-set full` 才使用。

默认核心 skill：

```text
ONBOARDING           → vibe-bootstrap / vibe-retrofit / vibe-discovery
EXEC                 → vibe-exec         → 最小、可回滚实施包装
XCHECK               → vibe-xcheck       → 正向/边界/负面/回归/sanity 验证
GUARD                → vibe-guard        → 风险、回滚、假设、残余风险
EVOLVE               → vibe-evolve       → 评估 lesson 是否晋升能力
COMPLETE 前          → vibe-memory-check → 校验一致性（不通过则阻断）
```

可选高级 skill（不属于 lean 默认安装面）：

```text
vibe-plan / vibe-alpha / vibe-review / vibe-debug / vibe-context / vibe-changelog
vibe-lessons / vibe-init / vibe-knowledge / vibe-omega / vibe-pipeline / vibe-git
```

按场景触发的最小集：

| 你正在做的事 | 触发 Skill | 必须更新 |
|---|---|---|
| 项目首次接入 | **vibe-bootstrap / vibe-retrofit / vibe-discovery** | registry / AGENTS draft / governance files |
| 普通实施 | **vibe-exec** | 按任务范围最小修改 |
| 安装/升级依赖、改 CI/scripts、构建命令变化 | EXEC（无专属 skill） | tech-stack.md（**真实命令**，禁止凭空生成 — L1） |
| 完成一个增量 / 审计与优化 | **vibe-xcheck** | 记录命令、场景、结果、缺口 |
| 调试 bug | **vibe-debug**（optional） | 仅在明确调试任务中使用 |
| 新增/重命名/删除模块、模块边界变化 | **vibe-guard** | architecture.md |
| 产品目标/范围/非目标变化 | **vibe-guard**（破坏性范围变更） | prd.md（必要时同步 architecture.md） |
| 完成提交、记录变更 | **vibe-changelog / vibe-git**（optional） | docs/AI_CHANGELOG.md（不写 memory-bank） |
| 同一类失败第 2 次 / 累积失败 | **vibe-lessons**（optional） → **vibe-evolve** | docs/LESSONS.md（**不写 memory-bank**），评估晋升 L4 |
| 任务收尾 | **vibe-memory-check** | 校验 memory-bank 引用一致；不通过则阻断 COMPLETE |
| 长会话续跑 / 上下文恢复 | **vibe-context**（optional） | activeContext.md（覆写焦点 / 追加假设） |
| 沉淀决策与约定 | **vibe-knowledge**（optional） | architecture.md（ADR）或 docs/LESSONS.md |
