# LESSONS Rules

## 文件职责
- `docs/LESSONS.md`：主经验库，只保留索引和活跃窗口。
- `docs/LESSONS_ARCHIVE.md`：归档库，存放默认不进入活跃窗口的历史条目。
- `evolution/lesson-index.json`：机器可读 lesson 索引。
- `evolution/promotion-log.md`：lesson 晋升记录。

## 默认读取协议
1. 先读取 `docs/LESSONS.md` 的 `Active Summary` 和 `索引`。
2. 默认展开所有 `Pinned` 条目 + 最近 `5~10` 条 `活跃` 条目。
3. 命中标签 / 关键词 / 影响文件时，再展开更早条目或 archive。
4. 禁止默认通读全文和 archive。

## 索引规则
索引列固定为：`#`、`标题`、`类型`、`成熟度`、`标签`、`优先级`、`状态`。
状态只允许：`活跃`、`已归档`、`Pinned`。

### 类型（type，5 类 MECE）
每条 lesson 必须归入恰好一类：

| 类型 | 含义 | 典型示例 |
|---|---|---|
| `model` | 实体定义、数据结构、关系图 | "memory-bank 五文件的字段契约" |
| `decision` | 技术选型、架构决策及理由 | "AGENTS.md 拆 Map + Reference 而非单文件" |
| `guideline` | 推荐做法 / 禁止做法（含 recommend/avoid） | "命令必须来自真实文件" |
| `pitfall` | 已知风险、故障模式、排查步骤 | "Skill frontmatter 与正文不一致会被误触发" |
| `process` | 业务/工程流程、状态机、操作步骤 | "MEMORY_CHECK 失败必须阻断 COMPLETE" |

### 成熟度（maturity，3 级 + 自动衰减）
| 级别 | 进入条件 | 含义 |
|---|---|---|
| `draft` | 新提取，单一来源 | 一次性观察，未经验证 |
| `verified` | 在本仓库内已被复用或避免一次相同失败 | 单项目验证 |
| `proven` | 已固化为 Guard / XCheck / Skill / Template / Linter | 跨场景可信赖；通常对应 `promotion_status: promoted:*` |

衰减建议（由 `vibe-evolve` 在执行 `--write` 时评估）：

- `proven` 条目若 12 个月未被新工作流引用 → 建议降级 `verified`。
- `verified` 条目若 6 个月未被引用 → 建议降级 `draft`。
- `draft` 条目长期未引用 → 建议归档（写入 `LESSONS_ARCHIVE.md`）。

## 正文格式
```markdown
## L{n} 标题
- 类型：model | decision | guideline | pitfall | process
- 成熟度：draft | verified | proven
- 场景：...
- 风险：...
- 修复策略：...
- 可复用模式：...
- 建议升级为 Guard/XCheck/Skill 规则：...
```

## 自动归档规则
- 活跃条目软上限：12。
- 写入新条目后如果活跃条目 > 12，立即触发归档检查。
- 自动归档目标：压回 8~10。
- Pinned 不参与默认归档。

## 引用追踪闭环（v5.3）
为防止 lesson 库无限堆积、与实际工作流脱节，每条 lesson 在 `evolution/lesson-index.json` 中携带三个引用字段：

| 字段 | 含义 |
|---|---|
| `last_referenced` | 在扫描语料中出现的最近日期（`YYYY-MM-DD`，按同文件内最近一次 ISO 日期标题就近归属） |
| `reference_count` | 在扫描语料中累计出现次数 |
| `referenced_in` | 出现过 `L\d+` 提及的文件相对路径列表 |

**扫描语料**（excludes `docs/LESSONS.md`、`LESSONS_ARCHIVE.md`、`lesson-index.json` 自身以避免自引用）：

- `memory-bank/progress.md`、`activeContext.md`、`architecture.md`
- `docs/AI_CHANGELOG.md`
- `evolution/promotion-log.md`
- `plans/*.md`、`plans/**/*.md`（若仓库存在）

**写法约定**：在上述任意文件中以 `L\d+` 形式（裸 ID，如 `L7`）即可被扫描自动归属；如需更高准确性，可在条目附近写显式日期标题 `## 2026-05-12` 或同行包含 `YYYY-MM-DD`，scanner 会就近继承。

**维护命令**：

```bash
python scripts/check_memory_consistency.py --update-refs   # 扫描并回写 last_referenced / reference_count / referenced_in
python scripts/check_memory_consistency.py --strict        # 只读校验；漂移时 WARN
```

**checker 行为**：

- 活跃 / Pinned lesson 在扫描语料中零引用 → WARN「考虑归档或在下个任务中验证」。
- JSON 中 `last_referenced` / `reference_count` 与扫描结果漂移 → WARN「运行 `--update-refs` 刷新」。
- `--update-refs` 仅 merge 三个字段，其他字段（`type` / `maturity` / `promotion_status` 等）保持不变。

优先归档：
1. 已固化到 AGENTS.md。
2. 已固化到 SKILL.md。
3. 已固化到 Guard/XCheck/测试流程。
4. 长期低频且不再是最近活跃风险。

## 时间序日志标题前缀（v5.4）
为让 `grep "^## \[" <file> | tail -5` 可靠抽取最近时间线，所有按日期记录的产物文件统一使用以下标题语法：

```
## [YYYY-MM-DD] <kind> | <summary>
```

| 文件 | 默认 kind |
|---|---|
| `docs/AI_CHANGELOG.md` | `changelog` |
| `evolution/promotion-log.md` | `promote` |
| `memory-bank/progress.md` | `progress` |

允许的 kind 集合：`changelog | promote | lint | progress | evolve | ingest | decision`。

`check_memory_consistency.py` 对上述三个文件中以日期开头但不符合该格式的 `##` 标题发 WARN（非阻塞）。灵感来源：Karpathy LLM-Wiki gist 的 log.md 约定。

## 孤儿页面守护（v5.4）
两向绑定 catalog ↔ content：

- `docs/agents/*.md` 必须至少被 `AGENTS.md` 引用一次（Map → Reference 完整覆盖）。
- `memory-bank/*.md`（除 `memory-registry.yaml` 自身外）必须在 `memory-registry.yaml` 中被列出（catalog 必须涵盖事实文件）。

违反 → WARN，提示删除文件或补登记。
