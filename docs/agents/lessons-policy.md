# Lessons 治理策略

> **Layer B 摘要**
> - **何时该读**：LESSONS 阶段要决定什么该写、何时该抽到 archive、活跃窗口超软上限、需要跟踪某条 lesson 是否还被引用。
> - **包含内容**：写入触发条件 / 最小字段集；读取协议（默认 Pinned + 近 5~10 条）；治理规则（软上限 12、归档目标 8~10、已固化优先归档）；v5.3 引用追踪闭环的简要说明。
> - **不在此处**：index 列格式 / type / maturity 完整定义 / 引用追踪细则 → [../LESSONS_RULES.md](../LESSONS_RULES.md)；LESSON 晋升 Guard / XCheck / Skill 的阈值与路径 → [evolution-policy.md](evolution-policy.md)。

> 本文件展开 [AGENTS.md](../../AGENTS.md) §14。

## 何时写入 LESSONS

涉及失败、返工、高频模式、新风险、新约束时，必须写入或更新 [docs/LESSONS.md](../LESSONS.md)。

每条 lesson 至少包含：

- 场景。
- 风险。
- 修复策略。
- 可复用模式。
- 建议升级为 Guard / XCheck / Skill 的规则。

## 读取协议

- 先读 Active Summary 和索引。
- 默认展开全部 Pinned 和最近 5~10 条活跃 lessons。
- 不默认通读 [archive](../LESSONS_ARCHIVE.md)。
- 命中标签、关键词、模块、同类失败时再展开 archive。

## 治理规则

- 活跃 lessons 软上限为 12。
- 目标活跃窗口为 8~10。
- Pinned 不参与默认归档。
- 已固化为 AGENTS、Skill、Guard、XCheck 的 lessons 应优先归档。
- 详细规则见 [docs/LESSONS_RULES.md](../LESSONS_RULES.md)。

## 引用追踪闭环（v5.3）

在 EXEC/PLAN/CHANGELOG 等阶段产物（`memory-bank/progress.md`、`memory-bank/activeContext.md`、`docs/AI_CHANGELOG.md`、`evolution/promotion-log.md`、`plans/**/*.md`）中以裸 `L\d+` 形式（例如 `L7`）显式引用相关 lesson，`scripts/check_memory_consistency.py` 会扫描并将 `last_referenced` / `reference_count` / `referenced_in` 写回 `evolution/lesson-index.json`（执行 `--update-refs`）。

活跃 / Pinned lesson 在扫描语料中长期零引用，checker 会 WARN「建议归档或在下个任务中验证」——这是 active 窗口的自然瘦身机制。完整字段定义与维护命令见 [LESSONS_RULES.md](../LESSONS_RULES.md#引用追踪闭环v53)。

## 与 EVOLVE 的关系

LESSONS 是 L3 经验态 memory；EVOLVE 是判断哪些 L3 lesson 应该晋升为 L4 能力（Guard/XCheck/Skill/Template）。详见 [evolution-policy.md](evolution-policy.md)。
