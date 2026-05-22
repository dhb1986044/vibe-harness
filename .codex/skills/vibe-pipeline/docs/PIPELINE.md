# P6-A：标准流水线模板（One-command Runbook）

## 目标
把 vibecoding 的“澄清 → 规划 → 审查 → 执行 → 评测 → 提交 → 沉淀”固化成可复用流水线。

## 推荐流水线（默认）
1. **vibe-plan**：锁门禁，澄清必停（>=VIBE_CLARIFY_MIN）
2. **vibe-init / vibe-alpha**：产出 PRD + PLAN-ONLY + 落盘（memory-bank/ + plans/）
3. **vibe-review**：Staff Engineer 计划审查（P0/P1/P2）
4. **进入执行阶段（EXEC）**：允许写文件/跑命令
5. **实施**：按 plan 执行（必要时 vibe-debug）
6. **数据验证（可选）**：用数据验证关键假设
7. **vibe-git**：原子提交计划 + 执行提交
8. **vibe-omega**：审计（规范、落盘、回归、风险）
9. **vibe-knowledge**：沉淀到 memory-bank/architecture.md（ADR）或 docs/LESSONS.md

## One-command Runbook（建议做法）
“一个技能生成一份 runbook + 命令清单”，然后你按 runbook 逐步触发各 skill 或执行命令。
- 见：`vibe-pipeline` 技能
