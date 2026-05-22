# Deployment Checklist

- [ ] Back up old AGENTS.md.
- [ ] Copy `memory-bank/memory-registry.yaml`.
- [ ] Copy `evolution/lesson-index.json` and `promotion-log.md`.
- [ ] Install vibe skills under `.codex/skills` and `.claude/skills`.
- [ ] Enable Codex hooks in `~/.codex/config.toml`.
- [ ] Copy `.codex/hooks.json` to project or global config.
- [ ] Copy `.claude/settings.example.json` to `.claude/settings.json`.
- [ ] Run `python scripts/check_memory_consistency.py --strict`.
- [ ] Test one small task in Codex and Claude.
