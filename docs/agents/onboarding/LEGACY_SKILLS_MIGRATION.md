# 旧 vibe 技能迁移说明

| 旧技能 | v5 定位 |
|---|---|
| vibe-init | optional / source-only；新项目默认用 vibe-bootstrap |
| vibe-alpha | optional / source-only；普通执行默认用 vibe-exec |
| vibe-omega | optional / source-only；审计能力拆到 vibe-guard + vibe-xcheck + vibe-evolve + vibe-memory-check |

目标项目中如存在旧副本，可迁入 `_legacy` 观察后归档；源 harness 仓库保留这些 Codex 技能源码，默认 lean 安装不复制。
