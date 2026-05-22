# 上下文管理优化（Context Management）

## 目标
控制对话与上下文规模，避免长对话性能下降/混淆。

## 机制
- 每轮开始先读：`memory-bank/activeContext.md`
- 任何“新任务”：在 `activeContext.md` 「当前焦点」节覆写必要信息
- 当对话过长：执行“断档重启”
  - 追写 `activeContext.md` 「关键假设 / 未决问题」节
  - 开新会话从 `activeContext.md` 续跑

## 产物
- 仅追写 `memory-bank/activeContext.md`，不创建未在 `memory-bank/memory-registry.yaml` 注册的文件。
