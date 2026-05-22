# 项目模式选择指南

## 三种模式

1. `new_project`：新项目，用 `vibe-bootstrap`。
2. `vibe_managed_legacy`：已有 vibe-* 痕迹的老项目，用 `vibe-retrofit`。
3. `unmanaged_legacy`：纯人工历史项目，用 `vibe-discovery`。

## 判断流程

```text
是否有 AGENTS.md / memory-bank / docs/LESSONS.md？
  是 -> 是否使用过 vibe-*？
       是 -> vibe-retrofit
       否 -> 按已有项目治理评估
  否 -> vibe-discovery

是否是空项目或刚开始？
  是 -> vibe-bootstrap
```
