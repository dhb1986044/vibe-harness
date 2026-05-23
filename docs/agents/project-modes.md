# 项目模式与 harness 阶段（v5.6）

vibe-harness 在三类项目上有截然不同的接入策略。本文档定义如何识别模式、如何选择入口 skill、如何在四个 phase 之间渐进切档。

来源：v5.1 [PROJECT_MODES_GUIDE.md](../../archive/v5.1-source-snapshot/manuals/PROJECT_MODES_GUIDE.md) + v5.5 治理面整合（PR-1）。

## 1. 三类项目模式

| 模式 | 适用场景 | 入口 skill | 默认初始 phase |
|---|---|---|---|
| `new_project` | 空仓库 / 刚开始规划 / 从模板初始化 | `vibe-bootstrap` | `managed_harness`（可直接启用全量门禁） |
| `vibe_managed_legacy` | 已有 AGENTS.md / memory-bank / LESSONS / 旧 vibe-* | `vibe-retrofit` | `shadow_harness` → `soft_gate` → `managed_harness` |
| `unmanaged_legacy` | 纯人工历史项目，无任何 harness 痕迹 | `vibe-discovery` | `discovery_only`（只读侦察，不改代码） |

### 1.1 判定流程

```text
是否存在 AGENTS.md / memory-bank/ / docs/LESSONS.md 之一？
├── 是 → 是否使用过 vibe-*？
│        ├── 是 → vibe_managed_legacy（用 vibe-retrofit）
│        └── 否 → 视为 vibe_managed_legacy 兜底，但先用 vibe-retrofit 评估
└── 否 → 是空项目 / 全新规划吗？
         ├── 是 → new_project（用 vibe-bootstrap）
         └── 否 → unmanaged_legacy（用 vibe-discovery）
```

模式声明在 [memory-bank/memory-registry.yaml](../../memory-bank/memory-registry.yaml) 的 `project_mode` 字段。registry 不存在时默认视为 `unmanaged_legacy`，**禁止直接重构**，必须先 Discovery。

## 2. 四阶段 harness phase

每个项目在生命周期中沿四阶段渐进，由 `harness_phase` 字段控制：

| Phase | 含义 | hook 行为 | 何时切档 |
|---|---|---|---|
| `discovery_only` | 只读侦察期 | `warn_only`（永不 block） | unmanaged_legacy 起点；产出 memory-bank 草稿后晋升 |
| `shadow_harness` | 影子运行期 | `warn_only`（输出警告但不阻断） | memory-bank 初稿完成后；观察 1~2 周误报率 |
| `soft_gate` | 软门禁 | `block_governance_files`（仅治理面 block） | 误报率 ≤10% 且团队认可后 |
| `managed_harness` | 硬门禁 | `block_all_failures`（全量 block） | CI 稳定 + 测试覆盖充分后 |

### 2.1 阶段切档准则

- **晋升**：连续 N 轮任务无误报 + 团队评审通过 + 记录到 `docs/AI_CHANGELOG.md`。
- **降级**：发现严重阻塞性误报时，**允许临时降一档**（如 `managed_harness` → `soft_gate`），但必须同步登记 LESSONS 并触发 EVOLVE 评估规则修正。
- **跳档**：不允许跳档晋升（如直接 `discovery_only` → `managed_harness`）；但允许跳档降级用于紧急止损。

### 2.2 治理面 (governance_paths) 定义

`soft_gate` 阶段的 "治理面" 路径在 [memory-bank/memory-registry.yaml](../../memory-bank/memory-registry.yaml) 的 `governance_paths` 字段集中声明，与 [.github/instructions/governance.instructions.md](../../.github/instructions/governance.instructions.md) 的 `applyTo` 列表保持语义一致。

## 3. 入口 skill 与生命周期协议

入口 skill **只在项目接入期（initial onboarding）触发一次**，之后的所有日常任务回归标准生命周期：

```text
INIT → MEMORY_BOOTSTRAP → PLAN → ALPHA → REVIEW → EXEC → XCHECK → GUARD
     → CHANGELOG → LESSONS → EVOLVE → MEMORY_CHECK → COMPLETE
```

入口 skill 详见：

- [vibe-bootstrap](../../.claude/skills/vibe-bootstrap/SKILL.md)（新项目初始化）
- [vibe-retrofit](../../.claude/skills/vibe-retrofit/SKILL.md)（已有 vibe 项目升级）
- [vibe-discovery](../../.claude/skills/vibe-discovery/SKILL.md)（纯历史项目只读侦察）

## 4. 工具支持

- `python scripts/check_memory_consistency.py --print-phase`：打印当前 mode/phase JSON。
- `python scripts/check_memory_consistency.py --warn-only`：强制 warn-only 模式（discovery / shadow 阶段使用）。
- `python scripts/discover_project.py --write`：只读侦察脚本（PR-3 引入），生成 `*.draft.md`。
- `python scripts/install_vibe_harness.py --target <path> --mode <bootstrap|retrofit|discovery> --context-profile light --skill-set lean`：安装器（PR-3 引入，v5.7 默认轻量）。安装器不得复制缓存/本地产物；在 discovery/retrofit 下也要补齐缺失的 Copilot governance instruction 与 Claude Stop hook 设置，但不得覆盖目标项目已有配置。需要复现 v5.6 重治理安装时传 `--context-profile full --skill-set full`。

## 5. 衡量指标

- 活跃 LESSONS 数：8–10（软上限 12）
- Stop hook 误报率：≤10%（discovery/shadow 阶段允许更高）
- Memory check 失败率（每周）：跟踪并触发 EVOLVE

## 6. 与 v5.5 治理面的关系

v5.6 在 v5.5（Map + 三向同步 + lesson schema + reference tracking + log prefix lint）之上**新增**项目模式与 phase 切档能力，不替换任何 v5.5 既有机制。本仓库自身保持 `vibe_managed_legacy` + `managed_harness`，行为与 v5.5 完全一致。
