# 安全与完成标准

> **Layer B 摘要**
> - **何时该读**：准备 COMPLETE、出现高风险改动需要 GUARD、不确定某次删除 / 重命名 是否需先评估回滚、思考是否该跳过 MEMORY_CHECK。
> - **包含内容**：安全与完整性原则（不提交密钥 / 评估回滚 / 保护 in-progress）；完成清单（用户成功标准 + XCHECK + GUARD + CHANGELOG + LESSONS + EVOLVE + memory-bank 同步 + MEMORY_CHECK）；MEMORY_CHECK 阻断规则。
> - **不在此处**：GUARD 的输出模板 / XCHECK 检查项 → [lifecycle.md](lifecycle.md)；hook 脚本位置 → [hooks-and-commands.md](hooks-and-commands.md)；Guard / XCheck skill 本身 → `.claude/skills/vibe-guard/SKILL.md`、`.claude/skills/vibe-xcheck/SKILL.md`。

> 本文件展开 [AGENTS.md](../../AGENTS.md) §20 + §21。

## 安全与完整性

- 不得提交真实 token、密钥、cookie、私有凭证。
- `defaults.json` 只能保留空占位或假值。
- 输出摘要只能记录 `token_source`，不记录 token 值。
- 发布仓不得包含内部 memory、测试样本、实验资产，除非明确允许。
- 删除、重命名、迁移文件前必须评估回滚方案。
- 发现工作区已有他人改动时，先停下并确认，不得覆盖。

## 完成标准

只有同时满足以下条件，任务才算 COMPLETE：

- 用户成功标准已满足。
- XCHECK 已通过，或未执行原因和替代证据已明确记录。
- GUARD 已通过，或风险与缓解已明确记录。
- [docs/AI_CHANGELOG.md](../AI_CHANGELOG.md) 已更新，或说明为何无需更新。
- [docs/LESSONS.md](../LESSONS.md) 已更新/确认无需更新。
- EVOLVE 已判断是否需要晋升经验。
- [memory-bank/](../../memory-bank/) 已同步到当前状态。
- MEMORY_CHECK 已通过，或当前任务完全不涉及 memory/harness 且说明原因。

若任一项缺失，不得标记为 COMPLETE。

## MEMORY_CHECK 触发条件

任务结束前，如果存在以下任一文件变更，必须执行 [scripts/check_memory_consistency.py](../../scripts/check_memory_consistency.py) `--strict`：

```text
AGENTS.md
docs/agents/**
memory-bank/**
docs/LESSONS.md
docs/LESSONS_ARCHIVE.md
docs/LESSONS_RULES.md
docs/AI_CHANGELOG.md
evolution/**
.codex/skills/vibe-*/**
.claude/skills/vibe-*/**
scripts/hooks/**
scripts/sync_vibe_skills.py
```

失败不得 COMPLETE，必须回到 REVIEW 或 EXEC 修复。
