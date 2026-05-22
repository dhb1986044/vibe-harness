# Codex / Claude Hooks 说明

## Codex

- 在 `config.toml` 开启 `[features] codex_hooks = true`。
- hooks 可放在 `~/.codex/hooks.json`、`~/.codex/config.toml`、`<repo>/.codex/hooks.json`、`<repo>/.codex/config.toml`。
- 本模板使用 `SessionStart`、`UserPromptSubmit`、`PreToolUse`、`Stop`。
- `Stop` hook 成功时静默，失败时输出 `{"decision":"block","reason":"..."}`。

## Claude

- 本模板使用 `.claude/settings.json` 的 `Stop` hook。
- 失败时输出 `{"decision":"block","reason":"..."}`。
