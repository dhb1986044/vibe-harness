# Memory 模型

> **Layer B 摘要**
> - **何时该读**：MEMORY_BOOTSTRAP 阶段要决定读什么、需要区分 L1~L4 哪一层路径、设计新 skill / hook 时需参考触发矩阵、不确定某件事实应入 memory-bank 还是 LESSONS 。
> - **包含内容**：L1 会话态 / L2 项目态 / L3 经验态 / L4 能力态四层 memory 的位置、所有者与生命周期；vibe-* 治理四件套与功能 skill 的触发矩阵；MEMORY_BOOTSTRAP 必读清单。
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

## MEMORY_BOOTSTRAP 必读顺序

任务开始前，代理必须按以下顺序读取：

1. [AGENTS.md](../../AGENTS.md)：当前执行契约。
2. [memory-bank/memory-registry.yaml](../../memory-bank/memory-registry.yaml)：memory 索引地图。
3. [memory-bank/activeContext.md](../../memory-bank/activeContext.md)：当前焦点。
4. [memory-bank/progress.md](../../memory-bank/progress.md)：最近进展。
5. [memory-bank/architecture.md](../../memory-bank/architecture.md)：架构边界。
6. [memory-bank/tech-stack.md](../../memory-bank/tech-stack.md)：语言、依赖、真实命令来源。
7. [docs/LESSONS.md](../LESSONS.md)：Active Summary、Pinned、最近 5~10 条活跃 lessons。
8. [evolution/lesson-index.json](../../evolution/lesson-index.json)：lesson 晋升索引。

代理还应按需读取 [docs/agents/](.) 下的细则文档（lifecycle / lessons-policy / evolution-policy / safety-and-completion / hooks-and-commands）。

## 读取策略

- 默认不通读 `docs/LESSONS_ARCHIVE.md`。
- 命中标签、关键词、模块、同类失败时，再按需读取 archive。
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

> 本仓库代理**只能触发** `.codex/skills/vibe-*` 与 `.claude/skills/vibe-*` 中的 skill。禁止使用通用 skill 名（如 spec-driven-development、planning-and-task-breakdown 等）作为触发器。
>
> 治理四件套（`vibe-memory-check / vibe-guard / vibe-xcheck / vibe-evolve`）双源同步；其他 16 个 skill 仅在 `.codex/skills/` 中可用。

按生命周期阶段：

```text
INIT                 → vibe-init        → memory-bank/* 全部初始化（含 prd/architecture/tech-stack/activeContext/progress）
PLAN                 → vibe-plan        → activeContext.md（澄清 + 范围）
                       vibe-alpha       → activeContext.md + plans/feature-plan.md（功能演进）
REVIEW               → vibe-review      → 仅评审 plan，不写代码
EXEC                 → vibe-omega       → progress.md（实施后的审计 + v2 迭代；omega 不是 EXEC 本身的执行器）
                       vibe-pipeline    → 输出 runbook
                       vibe-debug       → bug 根因 + 最小修复
XCHECK               → vibe-xcheck      → progress.md 追加（XCHECK 通过后）
GUARD                → vibe-guard       → architecture.md（必要时 prd.md）
CHANGELOG            → vibe-changelog   → docs/AI_CHANGELOG.md（结构化追加）
LESSONS              → vibe-lessons     → docs/LESSONS.md（容量管控+归档）
EVOLVE               → vibe-evolve      → evolution/lesson-index.json
COMPLETE 前          → vibe-memory-check → 校验一致性（不通过则阻断）
辅助                 → vibe-context     → activeContext.md 「关键假设 / 未决问题」
                       vibe-knowledge   → 知识沉淀到 architecture.md / LESSONS.md
                       vibe-git         → 提交纪律 + plans/commit-plan.md
```

按场景触发的最小集（**只列本仓库真实可用的 vibe-* skill**）：

| 你正在做的事 | 触发 Skill | 必须更新 |
|---|---|---|
| 项目首次启动 / 首次写 memory-bank | **vibe-init** | memory-bank/ 全部 5 个文件 |
| 接到新功能需求 / 大任务拆解 | **vibe-alpha** + **vibe-plan** | activeContext.md（+ plans/feature-plan.md）。决策：已有 prd.md 且为“功能演进”选 vibe-alpha；任何需“先澄清后动手”的需求选 vibe-plan |
| 审查计划是否合理 | **vibe-review** | 仅评审，不落盘 |
| 安装/升级依赖、改 CI/scripts、构建命令变化 | EXEC（无专属 skill） | tech-stack.md（**真实命令**，禁止凭空生成 — L1） |
| 完成一个增量 / 审计与优化 | **vibe-omega** → **vibe-xcheck** | progress.md（XCHECK 通过后）。vibe-omega = EXEC 后的审计 + v2 计划生成，不是 EXEC 执行器 |
| 调试 bug | **vibe-debug** | progress.md（修复记录） |
| 新增/重命名/删除模块、模块边界变化 | **vibe-guard** | architecture.md |
| 产品目标/范围/非目标变化 | **vibe-guard**（破坏性范围变更） | prd.md（必要时同步 architecture.md） |
| 完成提交、记录变更 | **vibe-changelog** + **vibe-git** | docs/AI_CHANGELOG.md（不写 memory-bank） |
| 同一类失败第 2 次 / 累积失败 | **vibe-lessons** → **vibe-evolve** | docs/LESSONS.md（**不写 memory-bank**），评估晋升 L4 |
| 任务收尾 | **vibe-memory-check** | 校验 memory-bank 引用一致；不通过则阻断 COMPLETE |
| 长会话续跑 / 上下文恢复 | **vibe-context** | activeContext.md（覆写焦点 / 追加假设） |
| 沉淀决策与约定 | **vibe-knowledge** | architecture.md（ADR）或 docs/LESSONS.md |
