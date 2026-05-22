# Codex / Claude Hooks 配置说明

## Codex

1. 启用 feature：

```toml
[features]
codex_hooks = true
```

2. 使用 `.codex/hooks.json` 或 `~/.codex/hooks.json`。

3. 推荐事件：

- SessionStart
- UserPromptSubmit
- Stop
- PreToolUse 可选

Stop 失败返回 `decision: block`，让 Codex 继续修复。

## Claude

使用 `.claude/settings.json` 的 Stop hook 调用：

```bash
python scripts/hooks/memory_stop_guard.py
```
