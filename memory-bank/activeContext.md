# 当前上下文

## 当前焦点
- 任务：harness 默认 skill 面瘦身 v5.8 提交发布。
- 目标：将已完成的默认 lean skill 面收窄变更提交并推送到 `origin/main`；保留 `.codex/skills/vibe-*` 源码与 `--skill-set full` 兼容路径。

## 范围
- 包含：AGENTS、安装器、docs/agents、README、CHANGELOG、LESSONS、memory、commit plan、git commit/push。
- 不包含：修改外部项目、删除缓存、强推或重写远端历史。

## 假设 / 风险
- 默认按 `light` 启动；`L0-L3` 决定 profile 和 skill 面。
- 旧项目缺少 `read_policy.profiles` 时只 WARN，保持向后兼容。
- `--skill-set full` 仍复制完整 `.codex/.claude`；本次不删 skill 源码。
- 关联 lessons：L1 L2 L3 L7 L8 L10 L11 L12。
