---
name: vibe-lessons
description: >-
  项目经验教训库 docs/LESSONS.md 的生命周期管理器：负责 legacy 迁移、写入新教训、
  索引查询、容量管控与自动归档。当用户提到记录教训、查已知坑、历史错误、避坑、
  LESSONS 维护、教训归档、经验查询、反模式检索，或任何 AI 犯错后需要沉淀经验时，
  都应触发此技能。注意：本技能默认只消费索引和最近 5~10 条活跃教训，不默认通读全文。
metadata:
  short-description: "LESSONS.md 生命周期与索引消费协议"
  tags:
    - vibecoding
    - lessons
    - anti-pattern
    - knowledge
---

# vibe-lessons — 经验教训生命周期管理器

## 与治理四件套 vibe-evolve 的边界
- **vibe-lessons**（本技能）：负责教训的 **写入、索引、查询、容量管控、归档**。
- **vibe-evolve**：负责评估 lesson 的 **晋升**（L3 → L4）是否应固化为 Guard / XCheck / Skill / Template。
- 写入一条新教训 → 本技能；一条教训高频 ≡ 2 次 → 调 vibe-evolve。
- 本技能默认只消费索引和最近 5~10 条活跃教训，不默认通读全文。

管理项目根目录 `docs/LESSONS.md`、`docs/LESSONS_ARCHIVE.md`、`docs/LESSONS_RULES.md` 的完整生命周期：
**迁移 → 写入 → 索引 → 查询 → 自动归档**。

目标不是“多写几条日志”，而是让教训能被后续技能低成本消费。

---

## 管理对象
- 主库：`docs/LESSONS.md`
- 归档库：`docs/LESSONS_ARCHIVE.md`
- 规则文件：`docs/LESSONS_RULES.md`

优先读取项目根目录这些文件，不要把 skill 自带 `docs/` 目录误当成项目主数据源。

---

## 能力 0：legacy 迁移

如果项目根 `docs/LESSONS.md` 仍是旧格式，先迁移，再继续其它动作。

### 触发条件
- 没有 `Active Summary`
- 没有索引表
- lesson 编号重复或断号
- 没有 `docs/LESSONS_ARCHIVE.md`
- 没有 `docs/LESSONS_RULES.md`

### 迁移动作
1. 读取现有全部 lesson 标题与正文。
2. 修复重复编号或断号；这一步只允许在迁移时执行一次。
3. 为所有条目生成索引行：`# / 标题 / 标签 / 优先级 / 状态`。
4. 建立活跃窗口：
   - 默认保留最近 `8~10` 条为 `活跃`
   - 更早条目可作为“基线迁移归档”移入 archive
5. 写出 `docs/LESSONS_ARCHIVE.md` 与 `docs/LESSONS_RULES.md`。
6. 在 `docs/LESSONS.md` 头部补 `Active Summary` 和 `索引`。

迁移完成后，编号必须稳定，不再日常重排。

---

## 能力 1：查询已有教训

当用户或其他技能需要检查“是否有已知坑”时，提供低 token 成本的查询服务。

### 默认读取协议
1. 先读 `docs/LESSONS.md` 的 `Active Summary`。
2. 再读索引表。
3. 默认返回：
   - 所有 `Pinned`
   - 最近 `5~10` 条 `活跃`
4. 如果当前任务命中标签 / 关键词 / 影响文件，再按需展开相关旧条目或 archive。
5. 不默认通读全文。

### 输出格式
- 优先输出：`编号 + 标题 + 标签 + 优先级 + 状态`
- 只有用户明确需要详情时，才展开正文
- 回答中优先引用 lesson id，例如 `L9`、`L14`

---

## 能力 2：写入新教训

当 AI 修复了一个错误，或人工审查发现了反模式时，写入新条目。

### 流程
1. 先执行 legacy 检查；若未迁移，先迁移。
2. 读取索引，确定最新编号。
3. 做去重检查：至少比较标题关键词、标签、风险摘要、影响文件或模块。
4. 从以下标签中选取 1-2 个：
   - `[Prompt]`
   - `[PP]`
   - `[Schema]`
   - `[Process]`
   - `[Rule]`
   - `[Skill]`
5. 选定优先级：`P0 / P1 / P2`
6. 以仓库当前紧凑格式写入：

```markdown
## L{n+1} 标题
- 场景：...
- 风险：...
- 修复策略：...
- 可复用模式：...
- 建议升级为 Guard/XCheck 规则：...
```

7. 更新索引表中的标签、优先级和状态。
8. 写入完成后立即执行容量检查与自动归档。

如果只是同一反模式的变体，优先更新已有条目，而不是新开编号。

---

## 能力 3：自动归档

防止 `LESSONS.md` 无限增长导致读取成本失控。

### 规则
- 活跃条目软上限：`12`
- 触发时机：写入新条目后如果活跃条目 `> 12`
- 目标窗口：压回 `8~10`
- `Pinned` 条目不参与默认归档

### 归档优先级
优先归档满足以下任一条件的条目：
1. 已固化到 `AGENTS.md`
2. 已固化到某个 `SKILL.md`
3. 已固化到 Guard / XCheck / 测试流程
4. 长期低频，不再是最近活跃风险

### 归档动作
1. 将正文移到 `docs/LESSONS_ARCHIVE.md`
2. 主库索引保留该行，状态改为 `已归档`
3. 在 archive 批次说明中记录归档原因

---

## 与 AGENTS 的配合

如果仓库 `AGENTS.md` 规定“INIT / REVIEW / XCHECK 前必须读 LESSONS”，本技能应帮助消费者遵守以下协议：
- 只读索引 + 最近 `5~10` 条活跃
- 命中标签 / 关键词时才展开旧条目
- 任务与长期高风险规则相关时，优先读取 `Pinned`

---

## 评估重点
修改本技能后，至少验证以下 4 件事：
1. 能把 legacy `LESSONS.md` 迁成“索引 + 活跃 + archive”结构
2. 查询时是否先读索引，而不是全文
3. 写入后是否会自动做容量检查与归档
4. 其它技能或人工查询时，是否能稳定引用 lesson id

---

## 参考文件
- `docs/LESSONS.md`
- `docs/LESSONS_ARCHIVE.md`
- `docs/LESSONS_RULES.md`
