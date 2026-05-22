# 知识沉淀（持续学习配置）

## 目标
把每次纠错转化为规则与复用资产，降低重复犯错。

## 建议落点（工程内）
- `memory-bank/architecture.md`：架构决策与 ADR（可审计）
- `memory-bank/progress.md`：进展与事实
- `docs/LESSONS.md`：反模式 / 失败教训（调 vibe-lessons）

## 规则：纠错即落盘
每次你纠正 AI 后，追加：
- 发生了什么（症状）
- 正确做法（规则）
- 如何自动检测（测试/脚本/检查项）

## 维护：每周一次“清理与复训”
- 删除过时规则
- 合并重复规则
- 把高频错误提升为“门禁规则”（写入 SYSTEM CONTRACT / vibe-plan）
