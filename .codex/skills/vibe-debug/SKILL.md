---
name: vibe-debug
description: "调试修复：基于日志/堆栈定位根因，给出最小修复+验证步骤，必要时再进入 EXEC。"
metadata:
  short-description: "Debug assistant"
  tags:
    - vibecoding
    - debug
    - fix
---

# vibe-debug（AI 调试助手）

## 工作流
1) 先澄清（复现/环境/期望）
2) PLAN-ONLY：根因假设 + 验证步骤
3) 用户授权 EXEC 后：最小修复 + 运行测试/验证命令
4) 落盘：
   - 修复过程与验证结果 → 追加 `memory-bank/progress.md`
   - 可复用的根因/防范点 → **调用 vibe-lessons** 写入 `docs/LESSONS.md`

不创建 `PROJECT_GUIDE` 或其他未注册文件。

## 与治理四件套的衔接
- 修复后需 EXEC 验证 → **vibe-xcheck**
- 同类 bug 反复出现 → **vibe-evolve** 评估晋升
