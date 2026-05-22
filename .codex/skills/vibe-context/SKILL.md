---
name: vibe-context
description: "上下文管理：把焦点/假设/未决问题追写到 memory-bank/activeContext.md，支持断档重启与最小上下文续跑。"
metadata:
  short-description: "Context management"
  tags:
    - vibecoding
    - context
    - briefing
---

# vibe-context（上下文管理）

## 何时用
- 对话太长、模型变慢
- 新任务开始需要“干净上下文”
- 需要把当前状态交接给新会话

## 输出位置（复用 memory-bank 已注册文件，不引入幽灵文件）
- **当前焦点、关键假设、下一动作** → 覆盖写到 `memory-bank/activeContext.md`
- **开放问题 / 待决项** → 追加到 `memory-bank/activeContext.md` 的「关键假设 / 未决问题」节
- **上下文摘要 briefing** → 仅输出到对话，不落盘为独立文件（需要交接时手动复制）

不创建 `briefing.md` / `open_questions.md` 等未在 `memory-registry.yaml` 注册的文件。
