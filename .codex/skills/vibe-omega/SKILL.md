---
name: vibe-omega
description: (AUTO-PERSIST) Omega audit gate. Persists findings and refined v2 artifacts into plans/ and memory-bank/progress.md.
metadata:
  short-description: Omega audit auto-persist
  tags: [vibecoding, omega, audit, memory-bank, auto-persist]
---

# vibe-omega (AUTO-PERSIST)

## Mandatory reading
- Read `docs/00_SYSTEM_CONTRACT.md`
- Follow `docs/30_OMEGA.optimizer.md`

## Auto-persist contract (hard)
Append `memory-bank/progress.md` with an Omega audit entry and write one refined artifact:
- `plans/feature-plan.v2.md` OR `plans/implementation-plan.v2.md` OR `plans/execution-prompt.v2.md`
Update `memory-bank/architecture.md` if key decisions change.

Fallback: output full file contents using ```path blocks.

## 示例

### 示例：审计与回归（不直接改代码，先出审计与改进计划）
**输入（用户）**
> 现在模型经常跳过澄清直接写代码，请审计并给出修复建议。

**你应该做**
1. 审计：触发链路、门禁规则、默认模板是否过宽。
2. 输出缺陷清单（按严重级别 P0/P1/P2）。
3. 输出 v2 修复计划（PLAN-ONLY）。
4. 落盘：`plans/audit-report.md` + `plans/implementation-plan.v2.md`

## Additional resources
- 规范与模板：`docs/`
- 核心协议：`docs/00_SYSTEM_CONTRACT.md`
