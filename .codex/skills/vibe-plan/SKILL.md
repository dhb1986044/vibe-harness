---
name: vibe-plan
description: "只读规划门禁：强制澄清>=VIBE_CLARIFY_MIN，输出 PLAN-ONLY，不写代码不执行命令。"
metadata:
  short-description: "Plan-only gate (read-only)"
  tags:
    - vibecoding
    - plan
    - gate
---

# vibe-plan（只读规划门禁）

## 与 vibe-alpha 的边界
- **vibe-plan**：只读规划门禁，适用于任何需“强制先澄清、禁止一上来写代码”的场景，不落盘 memory-bank。
- **vibe-alpha**：面向功能演进，会主动读 `memory-bank/*` 并追写 `prd/activeContext/progress` + `plans/feature-plan.md`。
- 如果用户需求是“新功能 / 需求变更”请改用 vibe-alpha；如果仅需“让模型先问后做”请用本技能。

## 目的
当你想强制模型先澄清、先规划，避免一上来写代码/跑命令时，使用本技能。

## 硬规则
- 本轮先提出 >= `VIBE_CLARIFY_MIN` 个澄清问题（默认 9）。
- 在用户回答或明确授权“按默认假设继续/直接进入规划”前：只能输出“澄清问题清单”。
- 规划阶段：只输出 PLAN-ONLY（每步带验证）；禁止直接写代码。
- 执行阶段：仅当用户明确说“进入执行阶段（EXEC）”或 `VIBE_EXEC_MODE=1` 才允许写文件/跑命令。

## 输出格式
- 澄清阶段：只输出问题清单
- 规划阶段：输出 PLAN-ONLY +（可选）path 块落盘内容
- 执行阶段：按计划逐步实现，并更新 `memory-bank/progress.md`

## 示例
**输入**
> vibe-plan：在现有地址解析中新增“门牌号不拆分，楼栋拆分”的规则

**输出**
- 先列出澄清问题（>=9），并停下等待用户答复
