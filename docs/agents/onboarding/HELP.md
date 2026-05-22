# 帮助文档

## 我应该用哪个模式？

- 新项目：bootstrap
- 已有 vibe 项目：retrofit
- 纯人工历史项目：discovery

## 为什么 memory check 失败？

常见原因：

- 缺少 memory-registry.yaml
- LESSONS 索引和正文不一致
- lesson-index.json 非法
- active lesson 超过软上限

## 可以先不阻断吗？

可以。使用 `--warn-only` 或将 `harness_phase` 设置为 `shadow_harness`。
