# README_DEPLOYMENT - vibe-harness v5.1 部署手册

## 1. 判断项目模式

| 模式 | 特征 | 安装命令 |
|---|---|---|
| 新项目 | 空仓库或刚开始 | `--mode bootstrap` |
| 已有 vibe 老项目 | 有 AGENTS / memory / lessons / vibe skills | `--mode retrofit` |
| 纯人工历史项目 | 无 AGENTS / 无 memory / 无 lessons | `--mode discovery` |

## 2. 安装命令

```bash
python scripts/install_vibe_harness.py --target /path/to/repo --mode discovery --dry-run
python scripts/install_vibe_harness.py --target /path/to/repo --mode discovery
```

## 3. 安装后检查

```bash
cd /path/to/repo
python scripts/check_memory_consistency.py --warn-only
```

新项目或 managed 项目：

```bash
python scripts/check_memory_consistency.py --strict
```

## 4. 启用 Codex Hooks

复制：

```bash
mkdir -p ~/.codex
cp .codex/hooks.json ~/.codex/hooks.json
```

并在 `~/.codex/config.toml` 中启用：

```toml
[features]
codex_hooks = true
```

## 5. 启用 Claude Hooks

```bash
mkdir -p .claude
cp .claude/settings.example.json .claude/settings.json
```

## 6. 老项目启用策略

老项目不要直接 hard gate：

1. discovery_only
2. shadow_harness
3. soft_gate
4. managed_harness

详见 `manuals/UNMANAGED_LEGACY_DISCOVERY_MANUAL.md` 与 `manuals/EXISTING_VIBE_PROJECT_RETROFIT_MANUAL.md`。
