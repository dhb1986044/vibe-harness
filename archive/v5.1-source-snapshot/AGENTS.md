# AGENTS.md v5.1 - Vibe Harness 执行契约

本文件是本仓库内所有编码代理的统一执行契约，适用于 Codex、Claude Code、Gemini CLI、GitHub Copilot 等代理。

本文件不是项目事实库，不应承载大量业务细节。项目事实、命令、架构、经验应分别进入 `memory-bank/`、`docs/LESSONS.md`、`evolution/` 与 `skills/`。

---

## 0. 定位：AGENTS 是什么

AGENTS.md 是代理工作的**执行宪法 + 生命周期协议 + 安全边界**。

它回答：

1. 代理做事时遵守什么优先级？
2. 代理如何读取项目记忆？
3. 代理如何规划、执行、验证和收尾？
4. 什么情况下必须风险评估？
5. 什么经验必须沉淀？
6. 什么条件下才允许标记任务完成？

它不回答：

1. 本项目所有业务细节是什么。
2. 所有历史经验正文是什么。
3. 每个技能的完整使用说明是什么。
4. 每个命令是否一定可运行。

这些内容应放入：

```text
memory-bank/                 项目事实记忆
docs/LESSONS.md              经验记忆
evolution/lesson-index.json  经验索引与晋升状态
.codex/skills/ 或 .claude/skills/  能力化技能
```

---

## 1. 全局与项目分层

### 1.1 全局 AGENTS

全局 AGENTS 放在个人或组织级配置中，只保存跨项目稳定原则，例如：

- 稳定性优先
- 先读后改
- 不发明命令
- 小步可回滚
- 验证后完成
- 经验要沉淀

### 1.2 项目 AGENTS

项目 AGENTS 放在仓库根或子目录下，保存本仓库的执行契约和项目特殊约束。

项目 AGENTS 可以覆盖或细化全局 AGENTS，但不得降低稳定性、安全性和可回滚性要求。

### 1.3 三类项目模式

本 harness 支持三类项目：

| 模式 | 适用场景 | 入口技能 | 默认策略 |
|---|---|---|---|
| `new_project` | 新仓库、空项目、刚开始规划 | `vibe-bootstrap` | 可直接初始化标准 harness |
| `vibe_managed_legacy` | 已有 vibe-*、AGENTS、memory、LESSONS 的老项目 | `vibe-retrofit` | 渐进升级，先兼容旧结构 |
| `unmanaged_legacy` | 纯人工历史项目，无 AGENTS、无 memory、无 lessons | `vibe-discovery` | 先只读考古，再草稿建档，再接管 |

项目当前模式记录在：

```text
memory-bank/memory-registry.yaml
```

若 registry 不存在，默认视为 `unmanaged_legacy`，必须先进入 Discovery，不得直接重构。

---

## 2. 总原则

### 2.1 优先级

```text
稳定性 > 可回滚性 > 可维护性 > 可解释性 > 性能 > 优雅性
```

发生取舍时，选择更稳定、更可回退、改动更小的方案。

### 2.2 行为原则

- **先读后改**：不确定时先读 README、脚本、CI、配置、文档、LESSONS。
- **不发明命令**：构建、测试、运行、发布命令必须来自仓库真实文件或用户明确提供。
- **小步修改**：优先局部、可控、可回滚的改动。
- **目标驱动**：只做用户目标需要的事，不做无关重构。
- **尊重真实架构**：不把理想模板强加给历史项目。
- **证据优先**：验证结果、命令来源、风险判断必须可追溯。
- **经验沉淀**：重复、高频、高风险经验必须进入 LESSONS，并判断是否晋升。

---

## 3. 生命周期状态机

默认任务流程：

```text
INIT
 -> MEMORY_BOOTSTRAP
 -> PLAN
 -> ALPHA
 -> REVIEW
 -> EXEC
 -> XCHECK
 -> GUARD
 -> CHANGELOG
 -> LESSONS
 -> EVOLVE
 -> MEMORY_CHECK
 -> COMPLETE
```

如任一门禁失败，必须回到前序阶段修正，不得跳过。

### 3.1 INIT

目标：

- 重述任务目标、约束、非目标。
- 判断项目模式：`new_project` / `vibe_managed_legacy` / `unmanaged_legacy`。
- 识别可能影响的文件、模块、脚本、配置。
- 明确成功标准。

若项目为 `unmanaged_legacy` 且没有 registry，不得直接改代码，必须先执行 Discovery。

### 3.2 MEMORY_BOOTSTRAP

按以下顺序读取：

1. `AGENTS.md`
2. `memory-bank/memory-registry.yaml`，若存在
3. `memory-bank/activeContext.md`
4. `memory-bank/progress.md`
5. `memory-bank/architecture.md`
6. `memory-bank/tech-stack.md`
7. `docs/LESSONS.md` 的 Active Summary、Pinned、最近活跃窗口
8. `evolution/lesson-index.json`，若存在

禁止默认通读 `LESSONS_ARCHIVE.md`。只有命中标签、关键词、模块或同类失败模式时，才按需展开。

### 3.3 PLAN

产出：

- 任务计划
- 风险点
- 验证方式
- 回滚思路
- 需要更新的 memory 文件

对于老项目，PLAN 阶段必须标记当前为：

```text
discovery_only / shadow_harness / soft_gate / managed_harness
```

### 3.4 ALPHA

目标：

- 做最小可工作的第一版。
- 优先满足核心成功标准。
- 不做大规模重构。
- 不引入未请求的抽象和依赖。

旧 `vibe-alpha` 的职责已并入本阶段或 `vibe-exec`。

### 3.5 REVIEW

目标：

- 审查正确性、边界条件、负面场景、兼容性、可维护性。
- 先找问题，再总结成果。
- 对核心逻辑、数据结构、接口和配置保持怀疑。

### 3.6 EXEC

目标：

- 落实最终改动。
- 补齐必要文档、脚本、配置和说明。
- 保持实现与 PLAN 一致。

### 3.7 XCHECK

XCHECK 是**结果验证门**，回答：

> 改完以后，事实是否成立？

必须覆盖：

- 正向 smoke
- 边界场景
- 负面输入
- 回归检查
- 受影响模块基本可用性
- 如涉及性能或大体量输出，做最小 sanity check

失败规则：

- XCHECK 失败必须回到 REVIEW 或 EXEC。
- 不允许跳过失败项直接完成。

### 3.8 GUARD

GUARD 是**风险控制门**，回答：

> 这次改动是否可能伤到系统，是否可回滚？

以下情况必须触发 GUARD：

- 核心逻辑重写
- 大规模删除或重构
- Schema / API / CLI 破坏性变更
- 依赖、工具链、构建链升级
- 发布脚本、manifest、hooks、AGENTS、memory、LESSONS 变更
- 测试覆盖不足但行为已变化

GUARD 必须输出：

- 风险等级：低 / 中 / 高
- 关键假设
- 回滚方案
- 尚未覆盖的残余风险

### 3.9 CHANGELOG

必须更新：

```text
docs/AI_CHANGELOG.md
```

至少包含：

- 日期
- 范围 / 模块
- 修改内容
- 修改原因
- 风险等级
- 回滚方式

对于 `discovery_only` 任务，可以记录为“仅文档草稿，无代码变更”。

### 3.10 LESSONS

必须判断是否新增或更新 lesson。

写入文件：

```text
docs/LESSONS.md
```

每条 lesson 至少包含：

- 场景
- 风险
- 修复策略
- 可复用模式
- 建议升级为 Guard/XCheck/Skill 的规则

若只是同一反模式的变体，优先更新已有 lesson，不新开编号。

### 3.11 EVOLVE

EVOLVE 是**经验晋升阶段**。

必须判断本次 lesson 是否应晋升为：

```text
Guard / XCheck / Skill / Template / Plugin / Archive
```

晋升条件：

- 重复出现
- 高风险
- 可复用
- 可自动化
- 有明确触发条件
- 有明确输入输出
- 能被验证

EVOLVE 产物：

```text
evolution/lesson-index.json
evolution/promotion-log.md
evolution/candidates/
```

### 3.12 MEMORY_CHECK

任务结束前必须执行 memory consistency 检查。

推荐命令：

```bash
python scripts/check_memory_consistency.py --strict
```

若当前项目处于 `discovery_only` 或 `shadow_harness`，可使用 warn-only：

```bash
python scripts/check_memory_consistency.py --warn-only
```

失败规则：

- managed_harness：失败不得 COMPLETE。
- soft_gate：治理文件失败不得 COMPLETE。
- shadow_harness：输出警告，但不强制阻断。
- discovery_only：只检查草稿文件是否生成。

### 3.13 COMPLETE

只有同时满足以下条件，任务才算完成：

- 成功标准已满足
- XCHECK 已通过或明确不适用
- GUARD 已通过或风险已记录
- CHANGELOG 已更新或说明不需要
- LESSONS 已判断是否更新
- EVOLVE 已判断是否晋升
- MEMORY_CHECK 已按当前模式通过
- memory-bank 已同步到当前状态

---

## 4. 三类项目接入策略

### 4.1 新项目：vibe-bootstrap

适用：空仓库、刚开始的项目。

允许：

- 初始化 AGENTS.md
- 初始化 memory-bank
- 初始化 docs/LESSONS.md
- 初始化 evolution
- 安装核心 vibe skills
- 配置 hooks

默认可直接进入 `managed_harness`。

### 4.2 已有 vibe 老项目：vibe-retrofit

适用：已有 AGENTS、memory、LESSONS、旧 vibe-* 技能。

要求：

- 不直接删除旧技能。
- 先将 `vibe-init / vibe-alpha / vibe-omega` 降级为 legacy adapter。
- 保留旧项目事实。
- 先运行 shadow，再 soft gate，最后 managed。

### 4.3 纯人工历史项目：vibe-discovery

适用：无 AGENTS、无 memory、无 lessons。

首次进入必须：

- 只读扫描
- 不改代码
- 生成 `.draft` 文件
- 标记 unknown
- 请求人工确认关键事实

禁止：

- 直接套新项目模板
- 直接重构
- 直接启用 blocking hooks
- 删除或重命名历史文件

---

## 5. Memory 结构

### L1 会话态 Memory

当前任务上下文，主要文件：

```text
memory-bank/activeContext.md
```

### L2 项目态 Memory

项目事实，主要文件：

```text
memory-bank/prd.md
memory-bank/architecture.md
memory-bank/tech-stack.md
memory-bank/progress.md
memory-bank/memory-registry.yaml
```

### L3 经验态 Memory

经验与教训：

```text
docs/LESSONS.md
docs/LESSONS_ARCHIVE.md
docs/LESSONS_RULES.md
```

### L4 能力态 Memory

已固化能力：

```text
.codex/skills/
.claude/skills/
evolution/candidates/
scripts/hooks/
```

---

## 6. 旧 vibe 技能迁移规则

旧技能处理：

```text
vibe-init  -> vibe-bootstrap / MEMORY_BOOTSTRAP
vibe-alpha -> ALPHA 阶段 / vibe-exec
vibe-omega -> vibe-guard + vibe-xcheck + vibe-evolve + vibe-memory-check
```

旧技能不得直接删除，先迁入：

```text
.codex/skills/_legacy/
.claude/skills/_legacy/
```

观察 1~2 周无触发后，可归档到：

```text
archive/legacy-skills/
```

---

## 7. Hooks 与自动门禁

### 7.1 Codex

Codex hooks 应启用：

```toml
[features]
codex_hooks = true
```

推荐事件：

- `SessionStart`：加载 memory bootstrap 提醒
- `UserPromptSubmit`：识别任务模式并提示 harness
- `Stop`：执行 memory consistency
- `PreToolUse`：可选，拦截危险命令

### 7.2 Claude Code

推荐配置：

- `Stop` hook：执行 memory consistency
- 失败时返回 block，让 Claude 继续修复

### 7.3 Hook 分阶段启用

```text
discovery_only: 不启用 block
shadow_harness: warn only
soft_gate: 仅治理文件 block
managed_harness: 全量 block
```

---

## 8. 仓库命令规则

代理必须从真实文件发现命令，例如：

- README
- Makefile
- package.json
- pyproject.toml
- requirements
- scripts
- CI 配置

所有命令都要记录来源。

禁止：

- 凭空发明命令
- 用不存在的脚本作为验证依据
- 用“应该可以”替代真实验证

---

## 9. 安全与完整性

- 不得提交真实 token、key、password。
- 不得将内网地址、敏感路径、生产配置暴露到公开发布包。
- 不得为了“看起来完整”而复制大包或无关资产。
- 对插件发布仓，必须区分源码仓与发布仓。
- 对历史项目，未知配置先标记 unknown，不擅自删除。

---

## 10. 默认行为

除非用户明确要求，否则默认：

- 先读后改
- 先小后大
- 先验证再结束
- 先记录再完成
- 先适配现状，不强推理想架构
- 先 warn，再 block，适用于老项目接管期
