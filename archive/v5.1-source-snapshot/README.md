# vibe-harness v5.1

一套面向多项目模式的 Agent Harness 模板，支持：

1. 新项目初始化：`vibe-bootstrap`
2. 已有 vibe-* 老项目升级：`vibe-retrofit`
3. 纯人工历史项目接入：`vibe-discovery`
4. 日常研发闭环：`AGENTS.md + XCHECK + GUARD + LESSONS + EVOLVE + MEMORY_CHECK`

## 快速开始

```bash
python scripts/install_vibe_harness.py --target /path/to/repo --mode discovery --dry-run
python scripts/install_vibe_harness.py --target /path/to/repo --mode discovery
```

模式选择见：`manuals/PROJECT_MODES_GUIDE.md`。

## 核心能力

- AGENTS.md v5.1 执行契约
- memory-bank 项目记忆
- LESSONS 经验库
- EVOLVE 自进化晋升
- Codex / Claude hooks 自动门禁
- 新项目、vibe 老项目、人工历史项目三种接入手册
