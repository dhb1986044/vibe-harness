---
name: vibe-alpha
description: "(AUTO-PERSIST) Feature evolution: requirement -> clarify -> plan-only. Updates memory-bank and writes plans/feature-plan.md."
metadata:
  short-description: Alpha plan-only auto-persist
  tags: [vibecoding, alpha, planning, memory-bank, auto-persist]
---

# vibe-alpha (AUTO-PERSIST)

## Mandatory reading
- Read `docs/00_SYSTEM_CONTRACT.md`
- Follow `docs/20_ALPHA.generator.md`
- Read `memory-bank/*` first (prd/architecture/tech-stack/activeContext/progress). If missing, stop and run vibe-init.

## Auto-persist contract (hard)
You MUST update:
- `memory-bank/prd.md` (AC/scope/change log if needed)
- `memory-bank/activeContext.md`
- append `memory-bank/progress.md`
And write:
- `plans/feature-plan.md`

If cannot write files, output full contents using ```path blocks.

## 示例

### 示例：需求变更/功能演进（仅输出计划）
**输入（用户）**
> 在现有地址解析里增加“门牌号不拆分、楼栋要拆分”的规则，并给出回归集。

**你应该做**
1. 读取当前 `memory-bank/*`，识别影响面（规则库/测试集/评测）。
2. 提出 >=9 个澄清问题（定义、优先级、样例、验收指标）。
3. 输出 PLAN-ONLY：方案对比 + 验证清单 + 回归集生成策略。
4. 落盘：`plans/feature-plan.md` + `memory-bank/progress.md`

## Additional resources
- 规范与模板：`docs/`
- 核心协议：`docs/00_SYSTEM_CONTRACT.md`
