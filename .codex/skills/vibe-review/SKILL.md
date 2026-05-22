---
name: vibe-review
description: "计划审查：以资深工程师视角审查 PLAN-ONLY，指出缺陷与修订方案（P0/P1/P2）。"
metadata:
  short-description: "Plan review (Staff Engineer)"
  tags:
    - vibecoding
    - review
    - plan
---

# vibe-review（计划审查）

## 硬规则
- 不写代码、不执行命令
- 只审查：目标/方案/影响面/验证/风险/回滚/提交策略
- 输出必须分级：P0/P1/P2，并给出“最小可行修订”
## 审查上下文
审查计划前必须先读取本项目根目录 `docs/LESSONS.md` 的 `Active Summary` 与索引表，按本项目实际命中的 lesson 编号检查计划是否触犯已知反模式：

- 命中标签 / 关键词 / 影响文件时，按需展开对应 lesson 正文。
- 不要假设 lesson 编号（不同项目的 L1/L2/L3 含义不同）；只引用本项目实际存在的编号。
- 默认不通读 `docs/LESSONS_ARCHIVE.md`，仅在标签命中时按需展开。

如果计划触犯了已知反模式，在审查报告中标注为 **P0** 缺陷并引用 lesson 编号（如 `本项目 L<N>`）。
## 输出
- `plans/plan-review.md`（审查报告）
- `plans/implementation-plan.v2.md`（修订后的计划，若需要）

## 参考
- 见 `docs/PLAN_REVIEW.md`
