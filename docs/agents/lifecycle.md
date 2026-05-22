# Lifecycle 详解

> **Layer B 摘要（按需快速定位）**
> - **何时该读**：开始新任务、需要确认某个生命周期阶段的产物 / 失败回退、设计阶段间过渡逻辑、排查阶段被跳过的原因时。
> - **包含内容**：INIT → MEMORY_BOOTSTRAP → PLAN → ALPHA → REVIEW → EXEC → XCHECK → GUARD → CHANGELOG → LESSONS → EVOLVE → MEMORY_CHECK → COMPLETE 每个状态的目标、必要产物、失败回退路径；XCHECK 与 GUARD 触发清单细则。
> - **不在此处**：阶段间钩子脚本配置 → [hooks-and-commands.md](hooks-and-commands.md)；MEMORY_CHECK 阻断与完成清单 → [safety-and-completion.md](safety-and-completion.md)；LESSONS / EVOLVE 阶段的写入规则 → [lessons-policy.md](lessons-policy.md) / [evolution-policy.md](evolution-policy.md)。

> 本文件展开 [AGENTS.md](../../AGENTS.md) §4 标准生命周期。AGENTS.md 仅列出状态名，本文件给出每个状态的目标、产物、失败回退。

## 完整状态序列

```text
INIT -> MEMORY_BOOTSTRAP -> PLAN -> ALPHA -> REVIEW -> EXEC -> XCHECK -> GUARD -> CHANGELOG -> LESSONS -> EVOLVE -> MEMORY_CHECK -> COMPLETE
```

简单问答可跳过落盘；只要涉及代码、脚本、配置、文档、技能、memory、lessons、发布、依赖，必须进入完整生命周期。

## INIT

目标：确认任务意图、约束、非目标、影响范围。

必须明确：

- 用户目标。
- 影响文件、模块、脚本。
- 成功标准。
- 不做什么。
- 是否涉及高风险操作。

如果目标不清晰，优先澄清；若可以安全做最小合理假设，可先按最保守路径推进并记录假设。

## MEMORY_BOOTSTRAP

详见 [memory-model.md](memory-model.md)。

## PLAN

产物：

- 实施步骤。
- 风险点。
- 验证方式。
- 回滚路径。
- 若任务较大，更新 `memory-bank/activeContext.md` 或新增计划文件。

要求：

- 计划必须可执行。
- 命令必须来自仓库真实文件，如 README、Makefile、package.json、pyproject.toml、CI、现有 scripts。
- 不为"看起来完整"添加无关重构。

## ALPHA

目标：先做最小可工作版本。

要求：

- 先满足核心成功标准。
- 不在 ALPHA 阶段做大规模重构。
- 保持改动小，可回退。

## REVIEW

目标：先找问题，再总结。

必须审查：

- 正确性。
- 边界条件。
- 负面输入。
- 可维护性。
- 兼容性。
- 是否违背已知 lessons。

## EXEC

目标：落实最终改动。

要求：

- 保持实现与 PLAN 一致。
- 补齐必要文档、脚本、配置、模板。
- 不静默扩大范围。
- 若发现计划不合理，回到 PLAN/REVIEW 修正。

## XCHECK

XCHECK 是"结果正确性验证门"。它回答：改完以后，事实是否成立？

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

## GUARD

GUARD 是"系统风险评估门"。它回答：这次改动会不会伤到系统？

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

## CHANGELOG

涉及仓库状态变化时，必须更新 [docs/AI_CHANGELOG.md](../AI_CHANGELOG.md)。

至少包含：

- 日期。
- 范围 / 模块。
- 修改内容。
- 修改原因。
- 风险等级。
- 验证方式。
- 回滚方式。

## LESSONS / EVOLVE / MEMORY_CHECK

详见 [lessons-policy.md](lessons-policy.md)、[evolution-policy.md](evolution-policy.md) 与 AGENTS.md §16。
