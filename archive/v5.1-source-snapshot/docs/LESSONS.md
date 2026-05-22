# Lessons

## Active Summary

- 默认读取范围：Pinned 条目 + 最近 5~10 条活跃条目
- 当前 Pinned：L1-L3
- 当前活跃窗口：L1-L5
- 归档库：docs/LESSONS_ARCHIVE.md
- 规则说明：docs/LESSONS_RULES.md

## 索引

| # | 标题 | 标签 | 优先级 | 状态 |
|---|---|---|---|---|
| L1 | 不得凭空发明命令 | [Process,Command] | P1 | Pinned |
| L2 | 未管理历史项目必须先 Discovery | [Legacy,Discovery] | P1 | Pinned |
| L3 | Memory 检查失败不得 COMPLETE | [Memory,Gate] | P1 | Pinned |
| L4 | 高频经验应晋升为 Guard/XCheck/Skill | [Evolve] | P1 | 活跃 |
| L5 | 老项目接管先 warn 后 block | [Legacy,Hook] | P1 | 活跃 |

## Active Lessons

## L1 不得凭空发明命令
- 场景：代理需要运行、测试、构建或发布项目。
- 风险：凭空构造命令会导致误验证或破坏环境。
- 修复策略：命令必须来自 README、Makefile、package.json、pyproject、CI 或用户明确提供。
- 可复用模式：所有项目都必须记录命令来源。
- 建议升级为 Guard/XCheck 规则：命令无来源时禁止作为验收依据。

## L2 未管理历史项目必须先 Discovery
- 场景：项目没有 AGENTS.md、memory-bank 或 lessons。
- 风险：直接重构会破坏历史隐式约定。
- 修复策略：先只读扫描，生成草稿 memory 与 discovery report。
- 可复用模式：纯人工历史项目先考古再接管。
- 建议升级为 Guard/XCheck 规则：无 registry 的老项目禁止直接 hard gate。

## L3 Memory 检查失败不得 COMPLETE
- 场景：任务修改 AGENTS、memory、LESSONS 或 evolution。
- 风险：长期记忆不一致会让后续 agent 读取错误上下文。
- 修复策略：COMPLETE 前运行 `python scripts/check_memory_consistency.py --strict` 或按模式 warn-only。
- 可复用模式：memory consistency 是任务结束门禁。
- 建议升级为 Guard/XCheck 规则：managed_harness 模式下失败必须 block。

## L4 高频经验应晋升为 Guard/XCheck/Skill
- 场景：同一失败模式反复出现。
- 风险：经验只记录不晋升会造成重复踩坑。
- 修复策略：通过 EVOLVE 评分，生成候选 Guard/XCheck/Skill。
- 可复用模式：LESSONS 是原料，Skill 是能力。
- 建议升级为 Guard/XCheck 规则：高频 lesson 必须进入 promotion-log。

## L5 老项目接管先 warn 后 block
- 场景：历史项目刚接入 hooks。
- 风险：直接 block 可能让研发无法继续。
- 修复策略：先 shadow_harness，再 soft_gate，最后 managed_harness。
- 可复用模式：老项目接管优先旁路观察。
- 建议升级为 Guard/XCheck 规则：未过 shadow 观察期不得全量 hard gate。
