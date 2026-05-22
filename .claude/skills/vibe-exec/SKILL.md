---
name: vibe-exec
description: Perform minimal, reversible implementation work after PLAN/ALPHA. Optional execution skill that wraps the EXEC lifecycle stage with rollback discipline.
---

# vibe-exec

Use after PLAN / ALPHA / REVIEW, when ready to make the actual code change.

## 硬性约束

- **最小改动**：只做计划中明确的事，不引入未请求的抽象或依赖。
- **保留架构**：不重写、不重构核心逻辑。
- **可回滚**：每个改动都能在 5 分钟内 revert。
- **不混合改动**：格式化与行为修改分离提交。

## 执行步骤

1. 复述本次 EXEC 的最小目标与受影响文件列表。
2. 按文件做外科手术式修改（read-before-edit）。
3. 每完成一个文件即跑相关测试 / lint。
4. EXEC 完毕进入 **XCHECK** 阶段：
   - 正向 smoke
   - 边界
   - 负面输入
   - 回归检查
   - 受影响模块 sanity
5. XCHECK 通过后进入 **GUARD** 风险评估（高风险改动必须）。

## 验收

- 改动范围与 PLAN 一致，无意外膨胀。
- XCHECK 全部通过。
- 已记录回滚方案（修改文件清单 + revert 命令）。

参考：[docs/agents/lifecycle.md](../../../docs/agents/lifecycle.md)
