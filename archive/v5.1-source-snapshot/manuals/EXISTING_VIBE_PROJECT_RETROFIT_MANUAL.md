# 已有 vibe 老项目升级手册：vibe-retrofit

目标：平滑升级已有 AGENTS / memory / lessons / skills。

原则：不直接删除旧技能，不直接覆盖旧 AGENTS。

步骤：

1. 备份旧 AGENTS 与 skills。
2. 生成 `memory-registry.yaml`。
3. 生成或修复 `lesson-index.json`。
4. 将 `vibe-init / vibe-alpha / vibe-omega` 移入 `_legacy`。
5. 安装核心 v5 skills。
6. hooks 先 warn-only，观察 1~2 周。
7. 再进入 soft_gate / managed_harness。
