# vibe-harness-v5 部署说明

## 1. 文件结构

```text
AGENTS.md
memory-bank/
docs/
evolution/
scripts/
  context_budget.py
  check_memory_consistency.py
  evolve_lessons.py
  hooks/
.codex/
  config.toml.example
  hooks.json
  skills/
.claude/
  settings.example.json
  skills/
templates/
```

## 2. 安装到已有项目

推荐用安装器，默认轻量上下文与 lean skill set：

```bash
python scripts/install_vibe_harness.py --target <project-root> --mode retrofit --context-profile light --skill-set lean
python scripts/context_budget.py --profile light --json
python scripts/check_memory_consistency.py --strict
```

如需复现 v5.6 重治理形态，显式传 `--context-profile full --skill-set full`。

## 3. Codex 配置

### 3.1 启用 hooks

将以下内容加入 `~/.codex/config.toml`：

```toml
[features]
codex_hooks = true
```

### 3.2 Hook 位置

Codex 支持在活跃配置层旁边发现 `hooks.json` 或 `config.toml` 内联 hooks。推荐优先使用：

```text
~/.codex/hooks.json
<repo>/.codex/hooks.json
```

本模板提供 `<repo>/.codex/hooks.json`。如果要全局生效，可复制到：

```bash
mkdir -p ~/.codex
cp .codex/hooks.json ~/.codex/hooks.json
```

### 3.3 Codex Stop Hook 行为

`Stop` hook 会执行：

```bash
python scripts/check_memory_consistency.py --strict
```

失败时返回：

```json
{"decision":"block","reason":"..."}
```

这会让 Codex 继续一轮修复，而不是假完成。

## 4. Claude Code 配置

复制示例配置：

```bash
mkdir -p .claude
cp .claude/settings.example.json .claude/settings.json
```

`Stop` hook 会调用：

```bash
python3 scripts/hooks/memory_stop_guard.py
```

失败时返回 `decision:block`，阻止 COMPLETE。

## 5. 验证

```bash
python scripts/check_memory_consistency.py --strict
python scripts/context_budget.py --profile light --json
python scripts/evolve_lessons.py --write
python scripts/check_memory_consistency.py --strict
```

预期第一条命令输出：

```text
PASS: memory consistency check passed
```

## 6. 从 v4.3 迁移到 v5

推荐顺序：

1. 先提交 `memory-registry.yaml` 与 `lesson-index.json`，不改现有逻辑。
2. 人工 diff 现有 `docs/LESSONS.md` 和模板，确认活跃窗口是否需要压缩。
3. 安装 `vibe-memory-check`、`vibe-evolve`、`vibe-guard`、`vibe-xcheck`。
4. 配置 Codex/Claude hooks。
5. 用 v5 `AGENTS.md` 替换旧版。
6. 执行 `python scripts/check_memory_consistency.py --strict`。
7. 用一次小任务测试 Stop hook 是否会在失败时阻断。

## 7. 回滚

- 删除 `.codex/hooks.json` 或关闭 `~/.codex/config.toml` 中的 `codex_hooks`。
- 删除 `.claude/settings.json` 中的 hooks。
- 恢复旧版 `AGENTS.md`。
- 保留 `docs/LESSONS.md` 与 `memory-bank`，不建议直接删除历史经验。
