# Evolution 晋升策略

> **Layer B 摘要**
> - **何时该读**：EVOLVE 阶段要决定某条 lesson 能否晋升为 Guard / XCheck / Skill / Template、需要选择晋升的载体、评估衰减信号（长期未引用）、避免 skill 膨胀。
> - **包含内容**：五项晋升判断检查项；maturity 与 type 作为晋升锰点与首选载体表；衰减阈值（3 级 × 频次）；反技能膨胀准则；v5.3 引用频次作为衰减信号。
> - **不在此处**：LESSONS 本身的写入 / 存放 / 字段格式 → [lessons-policy.md](lessons-policy.md) + [../LESSONS_RULES.md](../LESSONS_RULES.md)；Guard / XCheck 执行时机 → [lifecycle.md](lifecycle.md)；vibe-evolve skill 本身 → `.claude/skills/vibe-evolve/SKILL.md`。

> 本文件展开 [AGENTS.md](../../AGENTS.md) §15。

## 升级判断

每次任务结束前，必须判断本次 lesson 是否满足升级条件：

1. 是否重复出现 2 次以上？
2. 是否造成失败、返工、误改、不可回滚风险？
3. 是否可以转化为明确检查规则？
4. 是否可以转化为稳定执行流程？
5. 是否适合沉淀为 Guard、XCheck、Skill、Template 或 Plugin？

### Maturity 作为晋升锚点（v5.2+）

每条 lesson 还必须维护 `maturity ∈ {draft, verified, proven}` 字段：

- `draft`：新提取，单一来源 → 不进入晋升候选。
- `verified`：在本仓库被复用或避免一次相同失败 → 进入晋升候选（按下方"频次阈值"评估）。
- `proven`：已固化为 Guard / XCheck / Skill / Template / Linter → `promotion_status` 字段必须填写具体载体（如 `promoted:vibe-memory-check`）。

衰减建议（执行 `evolve_lessons.py --write` 时给出，不强制写入）：

- `proven` 条目 12 个月未被引用 → 建议降级 `verified`。
- `verified` 条目 6 个月未被引用 → 建议降级 `draft`。
- `draft` 条目长期未引用 → 建议归档到 `docs/LESSONS_ARCHIVE.md`。

### Type 作为晋升路径选择（v5.2+）

`type ∈ {model, decision, guideline, pitfall, process}` 决定首选晋升路径：

| type | 首选载体 |
|---|---|
| `pitfall` | XCheck / Linter |
| `guideline` | Guard / Skill 提示 |
| `process` | Skill / 生命周期阶段 |
| `decision` | Template / AGENTS.md / architecture.md（ADR） |
| `model` | memory-bank/architecture.md 或 memory-registry.yaml schema |

## 晋升路径

```text
LESSON -> PATTERN -> GUARD/XCHECK -> SKILL -> TEMPLATE/PLUGIN
```

## 反技能膨胀

- 单条低风险 lesson 不得直接生成新 skill。
- 新 skill 前必须先判断能否并入已有 skill、guard、xcheck 或 template。
- 项目特有经验优先留在项目 memory，不默认进入全局 skill。

## 必须更新的产物

- [evolution/lesson-index.json](../../evolution/lesson-index.json)
- [evolution/promotion-log.md](../../evolution/promotion-log.md)

若脚本存在，可执行：

```bash
python scripts/evolve_lessons.py --write
```

## 频次阈值

来自 [memory-bank/memory-registry.yaml](../../memory-bank/memory-registry.yaml) `promotion_policy`：

- lesson_to_xcheck_frequency: 2
- lesson_to_guard_frequency: 2
- lesson_to_skill_frequency: 3
- 高严重度立即晋升。

## 引用频次作为衰减信号（v5.3）

晋升只看「向上的能量」，衰减看「向下的能量」——后者由 [LESSONS_RULES.md §引用追踪闭环](../LESSONS_RULES.md#引用追踪闭环v53) 提供：

- `evolution/lesson-index.json` 中每条 lesson 携带 `last_referenced` / `reference_count` / `referenced_in`。
- `python scripts/check_memory_consistency.py --update-refs` 扫描工作流语料并回写这三个字段。
- `--strict` 模式遇到活跃 / Pinned lesson 零引用或字段漂移会 WARN，但不阻断 COMPLETE。
- 当某条 `verified` lesson 满足"频次 ≥ 阈值 且 `last_referenced` 在 6 个月内"时，应提名晋升 `proven`；满足"长期零引用 且 已固化"时，应提名归档。最终决策仍由 `vibe-evolve` 加人工评审。
