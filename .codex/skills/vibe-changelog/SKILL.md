---
name: vibe-changelog
description: "Flight Recorder：结构化追加 docs/AI_CHANGELOG.md（含评分+风险+文档引用）"
metadata:
  short-description: "Append structured AI changelog entries"
  tags:
    - vibecoding
    - stability
    - changelog
---

# vibe-changelog（黑匣子：文档-代码同步记录仪）

## 何时使用
任何**非平凡**代码变更完成后必须记录。

## 何时不用（跳过条件，任一满足即可）
- 纯注释 / 文档拼写修正 / 格式化无逻辑变化
- 单文件 trivial 补丁（如修复一个 typo、改一个常量值且无影响面）
- 仅 `.gitignore` / 编辑器配置等非业务文件改动
- AI_CHANGELOG.md 自身的修订（避免递归记录）

## 目标
每次非平凡代码变更完成后：
- 强制记录依据文档（Code follows Doc）
- 强制写风险分析（Risk Analysis）
- 输出 Complexity Impact Score（0-10）
- 追加到 `docs/AI_CHANGELOG.md`

## 执行（文档化追加，无脚本依赖）
按 vibe-harness CHANGELOG 模板手动追加一条条目到 `docs/AI_CHANGELOG.md`。必填字段：

```markdown
## YYYY-MM-DD
- 范围：
- 变更：
- 原因：
- 风险等级：低/中/高
- 验证方式：
- 回滚方式：
```

## 规则
- 无 doc 依据也可记录，但 vibe-guard 会报警
- 核心/数据结构变更必须在“变更”节明确标识，并在“验证方式”包含 `python scripts/check_memory_consistency.py --strict`

## 与治理四件套的衔接
- 追加后调用 **vibe-memory-check**；如需教训记录调用 **vibe-lessons** → **vibe-evolve**。
