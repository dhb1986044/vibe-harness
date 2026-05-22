---
name: vibe-pipeline
description: "标准流水线生成器：输出 Runbook（阶段门禁→澄清→计划→复核→EXEC→提交→沉淀）与可执行命令清单。"
metadata:
  short-description: "Generate a vibecoding runbook"
  tags:
    - vibecoding
    - pipeline
    - runbook
---

# vibe-pipeline（标准流水线生成器）

## 你会做什么
- 读取当前工程的 `memory-bank/*`（若存在）与关键代码结构（只读）
- 生成一份 **Runbook**：从门禁配置到提交审计的“逐步执行清单”
- 生成对应命令建议（Windows PowerShell 优先）

## Runbook 必须显式集成治理四件套
生成的 runbook 中，以下节点必须显式调用对应 vibe-* skill：
- **EXEC 后** → 调用 `vibe-xcheck`
- **高风险变更前** → 调用 `vibe-guard`
- **COMPLETE 前** → 调用 `vibe-memory-check`
- **变更记录** → 调用 `vibe-changelog`
- **教训记录** → 调用 `vibe-lessons`、29 评估晋升 → `vibe-evolve`

## 输出
- `plans/runbook.md`
- （可选）`plans/parallel-plan.md`（若检测到可并行）

## 规则
- 本技能不直接写业务代码
- 如果信息不足，先提出澄清问题并停止

## 参考
- 见 `docs/PIPELINE.md` 与 `docs/RUNBOOK_TEMPLATE.md`
