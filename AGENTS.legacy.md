# AGENTS.md v5 - Agent Harness 执行契约

本文件是本仓库所有编码代理的仓库级执行契约。适用于 Codex、Claude Code、Gemini CLI、GitHub Copilot、OpenClaw 等代理。

## 0. 定位：AGENTS 是什么

AGENTS.md 不是普通 README，也不是项目知识库。它是代理改变仓库状态前必须遵守的“行为契约”。

第一性原理：代理会改变系统状态，因此必须同时满足：

1. 知道目标与边界。
2. 知道仓库真实事实。
3. 知道历史经验和高频风险。
4. 能证明改动正确。
5. 能评估风险与回滚。
6. 能把新经验沉淀为下一次可复用能力。

因此，本仓库采用以下闭环：

```text
MEMORY_BOOTSTRAP -> PLAN -> EXEC -> XCHECK -> GUARD -> CHANGELOG -> LESSONS -> EVOLVE -> MEMORY_CHECK -> COMPLETE
```

## 1. 全局 AGENTS 与项目 AGENTS 分层

### 1.1 全局 AGENTS

全局 AGENTS 位于用户级配置目录，例如：

```text
~/.codex/AGENTS.md
~/.claude/CLAUDE.md 或 ~/.claude/AGENTS.md
~/.gemini/GEMINI.md
```

全局文件只写跨项目稳定原则，例如：

- 先读后改。
- 不发明命令。
- 最小可回滚改动。
- 验证后再完成。
- 不伪造仓库事实。

### 1.2 项目 AGENTS

项目 AGENTS 位于仓库根目录：

```text
AGENTS.md
```

项目 AGENTS 只写本仓库执行契约和本仓库特有规则。项目事实应放入 `memory-bank/`，经验应放入 `docs/LESSONS.md`，晋升索引应放入 `evolution/lesson-index.json`。

### 1.3 冲突规则

优先级从高到低：

```text
用户当前指令 > 系统/开发者指令 > 项目 AGENTS > 目录级 AGENTS.override.md > 全局 AGENTS > memory-bank > lessons/archive
```

若规则冲突，优先稳定性、可回滚性和用户明确目标。

## 2. 总原则

### 2.1 优先级

```text
稳定性 > 可回滚性 > 可维护性 > 可解释性 > 性能 > 优雅性
```

发生取舍时，选择更稳定、更小、更可回退的方案。

### 2.2 执行原则

- 先思考再编码：先确认目标、约束、成功标准。
- 简单优先：不用未来需求污染当前实现。
- 外科手术式改动：小步、局部、可回滚。
- 目标驱动：只做用户目标相关改动。
- 尊重真实架构：基于仓库现状，不强加理想架构。
- 先读后改：不确定时先读文件、脚本和文档。
- 不发明命令：构建、测试、运行命令必须来自仓库真实文档或脚本。
- 不伪造验证：没有执行的命令不得写成已验证。

## 3. Memory 分层模型

本仓库使用四层 memory：

```text
L1 会话态 memory：当前任务上下文，主要是 memory-bank/activeContext.md
L2 项目态 memory：架构、技术栈、命令、进度，主要是 memory-bank/*.md
L3 经验态 memory：失败模式、修复策略、复用模式，主要是 docs/LESSONS.md
L4 能力态 memory：已固化为 skills、guards、xchecks、templates 的能力
```

L3 不应无限堆积。高频、严重、可复用、可验证的 lessons 必须通过 EVOLVE 晋升为 L4。

## 4. 标准生命周期

所有非 trivial 任务按以下状态推进：

```text
INIT -> MEMORY_BOOTSTRAP -> PLAN -> ALPHA -> REVIEW -> EXEC -> XCHECK -> GUARD -> CHANGELOG -> LESSONS -> EVOLVE -> MEMORY_CHECK -> COMPLETE
```

允许简单问答跳过落盘，但只要涉及代码、脚本、配置、文档、技能、memory、lessons、发布、依赖，就必须进入完整生命周期。

## 5. INIT

目标：确认任务意图、约束、非目标、影响范围。

必须输出或内部明确：

- 用户目标。
- 影响文件、模块、脚本。
- 成功标准。
- 不做什么。
- 是否涉及高风险操作。

如果目标不清晰，优先澄清；若可以安全做最小合理假设，可先按最保守路径推进并记录假设。

## 6. MEMORY_BOOTSTRAP

任务开始前，代理必须按顺序读取：

1. `AGENTS.md`：当前执行契约。
2. `memory-bank/memory-registry.yaml`：memory 索引地图。
3. `memory-bank/activeContext.md`：当前焦点。
4. `memory-bank/progress.md`：最近进展。
5. `memory-bank/architecture.md`：架构边界。
6. `memory-bank/tech-stack.md`：语言、依赖、真实命令来源。
7. `docs/LESSONS.md`：Active Summary、Pinned、最近 5~10 条活跃 lessons。
8. `evolution/lesson-index.json`：lesson 晋升索引。

读取策略：

- 默认不通读 `LESSONS_ARCHIVE.md`。
- 命中标签、关键词、模块、同类失败时，再按需读取 archive。
- 若 `memory-registry.yaml` 缺失，任务仍可继续，但必须在 CHANGELOG/LESSONS 中记录 memory harness 未完整。

## 7. PLAN

产物：

- 实施步骤。
- 风险点。
- 验证方式。
- 回滚路径。
- 若任务较大，更新 `memory-bank/activeContext.md` 或新增计划文件。

要求：

- 计划必须可执行。
- 命令必须来自仓库真实文件，如 README、Makefile、package.json、pyproject.toml、CI、现有 scripts。
- 不为“看起来完整”添加无关重构。

## 8. ALPHA

目标：先做最小可工作版本。

要求：

- 先满足核心成功标准。
- 不在 ALPHA 阶段做大规模重构。
- 保持改动小，可回退。

## 9. REVIEW

目标：先找问题，再总结。

必须审查：

- 正确性。
- 边界条件。
- 负面输入。
- 可维护性。
- 兼容性。
- 是否违背已知 lessons。

## 10. EXEC

目标：落实最终改动。

要求：

- 保持实现与 PLAN 一致。
- 补齐必要文档、脚本、配置、模板。
- 不静默扩大范围。
- 若发现计划不合理，回到 PLAN/REVIEW 修正。

## 11. XCHECK

XCHECK 是“结果正确性验证门”。它回答：改完以后，事实是否成立？

必须覆盖：

- 正向最小可用场景。
- 边界场景。
- 负面输入。
- 回归检查。
- 受影响模块基本可用性。
- 如涉及性能或大文件，做最小性能 sanity check。

失败规则：

- XCHECK 失败必须回到 REVIEW 或 EXEC。
- 不允许跳过失败项直接 COMPLETE。
- 无法执行的检查必须说明原因、残余风险和替代证据。

示例：

- Python：`python -m py_compile`、`python scripts/quick_validate.py`。
- 插件：同步脚本 + 发布校验。
- memory：`python scripts/check_memory_consistency.py --strict`。
- 报表：检查文件体积、关键字段、样本数和摘要。

## 12. GUARD

GUARD 是“系统风险评估门”。它回答：这次改动会不会伤到系统？

以下情况必须触发 GUARD：

- 核心逻辑重写。
- 大规模删除或重构。
- Schema 变更。
- API 破坏性变更。
- 工具链、构建链、依赖升级。
- 安全、权限、token、密钥、出网配置变化。
- 发布仓、插件 manifest、marketplace、安装入口变化。
- 测试覆盖不足但行为已变化。

必须输出：

- 风险等级：低 / 中 / 高。
- 回滚方案。
- 关键假设。
- 尚未覆盖的残余风险。

无回滚方案的高风险改动不得直接完成。

## 13. CHANGELOG

涉及仓库状态变化时，必须更新：

```text
docs/AI_CHANGELOG.md
```

至少包含：

- 日期。
- 范围 / 模块。
- 修改内容。
- 修改原因。
- 风险等级。
- 验证方式。
- 回滚方式。

## 14. LESSONS

涉及失败、返工、高频模式、新风险、新约束时，必须写入或更新：

```text
docs/LESSONS.md
```

lesson 至少包含：

- 场景。
- 风险。
- 修复策略。
- 可复用模式。
- 建议升级为 Guard / XCheck / Skill 的规则。

读取协议：

- 先读 Active Summary 和索引。
- 默认展开全部 Pinned 和最近 5~10 条活跃 lessons。
- 不默认通读 archive。
- 命中标签、关键词、模块、同类失败时再展开 archive。

治理规则：

- 活跃 lessons 软上限为 12。
- 目标活跃窗口为 8~10。
- Pinned 不参与默认归档。
- 已固化为 AGENTS、Skill、Guard、XCheck 的 lessons 应优先归档。

## 15. EVOLVE

EVOLVE 是“经验升级阶段”。它回答：本次经验是否应该变成下一次的自动能力？

每次任务结束前，必须判断本次 lesson 是否满足升级条件：

1. 是否重复出现 2 次以上？
2. 是否造成失败、返工、误改、不可回滚风险？
3. 是否可以转化为明确检查规则？
4. 是否可以转化为稳定执行流程？
5. 是否适合沉淀为 Guard、XCheck、Skill、Template 或 Plugin？

晋升路径：

```text
LESSON -> PATTERN -> GUARD/XCHECK -> SKILL -> TEMPLATE/PLUGIN
```

禁止技能膨胀：

- 单条低风险 lesson 不得直接生成新 skill。
- 新 skill 前必须先判断能否并入已有 skill、guard、xcheck 或 template。
- 项目特有经验优先留在项目 memory，不默认进入全局 skill。

必须更新：

```text
evolution/lesson-index.json
evolution/promotion-log.md
```

若脚本存在，可执行：

```bash
python scripts/evolve_lessons.py --write
```

## 16. MEMORY_CHECK

MEMORY_CHECK 是 memory harness 的最终一致性门禁。

任务结束前，如果存在以下任一文件变更，必须执行：

```text
AGENTS.md
memory-bank/**
docs/LESSONS.md
docs/LESSONS_ARCHIVE.md
docs/LESSONS_RULES.md
docs/AI_CHANGELOG.md
evolution/**
.codex/skills/vibe-*/**
.claude/skills/vibe-*/**
scripts/hooks/**
```

标准命令：

```bash
python scripts/check_memory_consistency.py --strict
```

失败规则：

- 不得进入 COMPLETE。
- 必须回到 REVIEW 或 EXEC 修复。
- 修复后重新执行 MEMORY_CHECK。

## 17. Hook 自动门禁

### 17.1 Codex

如果当前环境支持 Codex Hooks，必须启用：

```toml
[features]
codex_hooks = true
```

推荐配置：

```text
~/.codex/hooks.json
<repo>/.codex/hooks.json
```

最低要求：

- `SessionStart`：注入 memory bootstrap 提醒。
- `UserPromptSubmit`：识别非 trivial 工程任务。
- `Stop`：执行 memory consistency；失败时返回 `decision: block` 让 Codex 继续修复。

### 17.2 Claude Code

推荐配置：

```text
.claude/settings.json
```

最低要求：

- `Stop` hook 调用 `scripts/hooks/memory_stop_guard.py`。
- 失败时返回 `decision: block`，阻止任务完成。

### 17.3 Hook 与 Skill 的关系

- Hook 负责兜底，不让代理忘记。
- Skill 负责告诉代理怎么检查和怎么修。
- Script 负责确定性判断。
- AGENTS 负责定义完成标准。

## 18. 仓库命令规则

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
- 没跑命令却写“已通过”。
- 因找不到命令就跳过验证。

若命令不明确，先查文档或脚本；仍不明确时，说明不确定性并执行最小安全检查，如语法检查、导入检查、dry-run。

## 19. 并行执行规则

仅在以下条件全部满足时允许并行：

- 每个任务有独立 branch 或 worktree。
- 不同代理不同时编辑同一文件。
- 共享改动必须经过 REVIEW、XCHECK、GUARD 再汇合。

禁止：

- 对同一关键模块静默并行修改。
- 存在跨任务依赖却不显式说明。
- 未验证直接合并并行结果。

## 20. 安全与完整性

- 不得提交真实 token、密钥、cookie、私有凭证。
- defaults.json 只能保留空占位或假值。
- 输出摘要只能记录 token_source，不记录 token 值。
- 发布仓不得包含内部 memory、测试样本、实验资产，除非明确允许。
- 删除、重命名、迁移文件前必须评估回滚方案。
- 发现工作区已有他人改动时，先停下并确认，不得覆盖。

## 21. 完成标准

只有同时满足以下条件，任务才算 COMPLETE：

- 用户成功标准已满足。
- XCHECK 已通过，或未执行原因和替代证据已明确记录。
- GUARD 已通过，或风险与缓解已明确记录。
- `docs/AI_CHANGELOG.md` 已更新，或说明为何无需更新。
- `docs/LESSONS.md` 已更新/确认无需更新。
- EVOLVE 已判断是否需要晋升经验。
- memory-bank 已同步到当前状态。
- MEMORY_CHECK 已通过，或当前任务完全不涉及 memory/harness 且说明原因。

若任一项缺失，不得标记为 COMPLETE。
