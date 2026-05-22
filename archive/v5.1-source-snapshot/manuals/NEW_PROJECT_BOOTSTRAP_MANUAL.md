# 新项目接入手册：vibe-bootstrap

目标：直接建立标准 harness。

步骤：

1. 解压部署包。
2. 复制 `AGENTS.md`、`memory-bank/`、`docs/`、`evolution/`、`scripts/`。
3. 安装 `.codex/skills` 与 `.claude/skills`。
4. 配置 hooks。
5. 运行 `python scripts/check_memory_consistency.py --strict`。

新项目可以较快进入 `managed_harness`。
