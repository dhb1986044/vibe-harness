# 当前上下文

## 当前焦点
- 任务：harness 默认上下文瘦身 v5.7。
- 目标：把默认 bootstrap 从约 52KB 改为 profile 驱动；默认 `light` 控制在约 12KB 内，同时保留 `full` 治理路径。

## 范围
- 包含：`AGENTS.md`、`memory-registry.yaml`、`scripts/{context_budget,check_memory_consistency,install_vibe_harness}.py`、`scripts/hooks/codex_session_start.py`、`docs/agents/*`、CHANGELOG、LESSONS、evolution、progress。
- 不包含：直接修改 `D:/workspace/wl/platform_design`；执行 git commit/push；删除已忽略缓存目录。

## 假设 / 风险
- 默认按 `light` 启动；治理路径、高风险、返工或 lessons/evolution 任务升到 `full`。
- 旧项目缺少 `read_policy.profiles` 时只 WARN，保持向后兼容。
- 关联 lessons：L1 L2 L3 L7 L8 L10 L11 L12。
