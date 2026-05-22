---
name: vibe-init
description: (AUTO-PERSIST) Initialize a project using vibecoding. Writes/updates memory-bank docs and a plan file automatically.
metadata:
  short-description: Vibe init auto-persist (intent->PRD->plan->memory-bank)
  tags: [vibecoding, init, prd, planning, memory-bank, auto-persist]
---

# vibe-init (AUTO-PERSIST)

## Mandatory reading
- Read `docs/00_SYSTEM_CONTRACT.md`
- Follow `docs/10_INIT.intent2prd.md`
- Use `memory-bank/` as source of truth

## Auto-persist contract (hard)
You MUST create/update:
- `memory-bank/prd.md`
- `memory-bank/architecture.md`
- `memory-bank/tech-stack.md`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `plans/implementation-plan.md`

If you cannot write files, output each file's full content in blocks labelled with path:
```path
<full file content>
```

## Gates
- Ask >=9 clarifying questions unless AC already explicit.
- Plan-only until approved.
- Persist immediately after producing PRD/Plan.

## 示例

### 示例 1：从原始意图到 PRD+计划（仅规划阶段）
**输入（用户）**
> 我想做一个“电力地址治理智能体”，从地址字段提取村/小区/楼栋，并输出置信度。

**你应该做**
1. 提出 >=9 个澄清问题（字段、输出格式、边界、验收标准）。
2. 输出 PLAN-ONLY（不写代码、不执行命令）。
3. 自动落盘（EXEC 前如果不能写文件，用 path 块输出内容）。

**落盘文件（默认）**
- `memory-bank/prd.md`
- `plans/implementation-plan.md`

### 示例 2：用户明确进入执行
**输入（用户）**
> 进入执行阶段（EXEC）

**你应该做**
- 按计划写代码/运行命令
- 每次关键变更追加 `memory-bank/progress.md`

## Additional resources
- 规范与模板：`docs/`
- 核心协议：`docs/00_SYSTEM_CONTRACT.md`
