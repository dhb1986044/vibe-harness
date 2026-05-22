---
name: vibe-knowledge
description: "知识沉淀：把决策与纠错写入 memory-bank/architecture.md（ADR）或 docs/LESSONS.md，不创建未注册文件。"
metadata:
  short-description: "Knowledge compounding"
  tags:
    - vibecoding
    - knowledge
    - docs
---

# vibe-knowledge（知识沉淀）

## 你会做什么
- 将本次纠错/决策转写为可复用规则
- 稳定架构决策（ADR） → 追加到 `memory-bank/architecture.md` 的「参考文档 / ADR」节
- 可复用反模式 / 失败教训 → **调用 vibe-lessons** 写入 `docs/LESSONS.md`
- 进展记录 → 追加 `memory-bank/progress.md`

## 输出位置选择表

| 知识性质 | 写到哪里 |
|---|---|
| 架构决策、不变量 | `memory-bank/architecture.md` |
| 反模式、失败教训 | `docs/LESSONS.md`（调 vibe-lessons） |
| 本次任务进展 | `memory-bank/progress.md` |

不创建 `PROJECT_GUIDE.md` 或未在 `memory-registry.yaml` 注册的幽灵文件。

## 与治理四件套的衔接
- 高频反模式 → **vibe-evolve** 评估是否晋升 L4。
