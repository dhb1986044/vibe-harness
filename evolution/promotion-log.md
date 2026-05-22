# Promotion Log

记录 LESSON -> Guard/XCheck/Skill/Template/Plugin 的晋升历史。

## [2026-05-12] promote | L9 Copilot 集成与三向同步 (v5.5)
- L9 `Copilot 集成与三向同步`：固化为
  - `scripts/sync_vibe_skills.py` 三向同步（`MIRRORS = {codex, copilot}`，`diff_one()` / `_write_mirror()` / `docs/` backup-restore）；
  - `scripts/check_memory_consistency.py` 的 `VIBE_SKILLS_MIRRORS` 多镜像遍历；
  - `.github/copilot-instructions.md` 指针化 + Copilot 特定约束；
  - `.github/instructions/governance.instructions.md` 通过 `applyTo` 被动注入治理提醒；
  - `AGENTS.md` §9/§10/§11/§12 加入 Copilot 触发面与无 hook 兜底说明；
  - `memory-bank/memory-registry.yaml` `skill_roots.copilot` + `agent_targets.copilot.memory_policy.repo_scope_forbidden: true`。
- 验证：`sync --check` PASS（codex + copilot 两路）；`check_memory_consistency.py --strict` PASS。

## [2026-05-06] promote | L1 / L2 / L3 初始固化
- L1 `不发明命令`：保留为 Pinned Guard。
- L2 `Memory check 失败不得完成`：已固化为 `vibe-memory-check` skill 与 Stop hook。
- L3 `AGENTS.md 是 Map 不是 Manual`：已固化为 v5.1 AGENTS.md 模板（127 行 Map 骨架 + `docs/agents/` 6 个子文档）+ `scripts/sync_vibe_skills.py` 治理四件套单源镜像 + `scripts/check_memory_consistency.py` 的 `check_referenced_paths()` L2 引用一致性检查。

## [2026-05-07] promote | L4 / L5 反模式清理与 ghost-file linter
- L4 `harness 模板不应打包业务专属 skill`：候选状态。已通过删除 4 个错位 skill（vibe-prompt / vibe-data / vibe-parallel / vibe-knowledge-modifier）执行一次“反模式清理”；尚未固化为门禁清单。若同类问题再现一次，则在 vibe-evolve 的“new skill admission”加一条预防性 checklist。
- L5 `Skill 三层一致性（description / SKILL.md 正文 / docs/）`：已固化为 `scripts/check_memory_consistency.py` 的 `check_referenced_paths()` 第 6 项 ghost-file linter。GHOST_PATTERNS = `[PROJECT_GUIDE, briefing.md, open_questions.md]`；NEGATION_CONTEXT 通过否定语境（不创建 / 未注册 / deprecated / removed / ghost 等）豁免合法的禁令声明行。

## [2026-05-12] promote | L6 / L7 lesson schema 与引用追踪闭环
- L6 `Lesson 需带 type+maturity 字段`：已固化为 v5.2 LESSONS schema + `check_memory_consistency.py` lesson-schema lint。变更点：
  - `docs/LESSONS_RULES.md` 增加 type（5 类 MECE）与 maturity（3 级）定义、新正文格式、衰减建议。
  - `docs/LESSONS.md` 索引扩为 7 列（增加 `类型`/`成熟度`），L1~L6 正文与索引同步补齐字段。
  - `evolution/lesson-index.json` schema_version 升级为 `v5.2`，每条 lesson 增加 `type` 与 `maturity` 字段。
  - `scripts/check_memory_consistency.py` 新增 `parse_lesson_bodies()` 与 lesson-schema lint：active/Pinned 缺失字段 → ERROR；索引与正文/索引与 JSON 漂移 → ERROR；draft 在活跃窗口超过 5 条 → WARN。
  - `docs/agents/evolution-policy.md` 引入 maturity 作为晋升锚点、type 作为晋升路径首选载体表。
  - `memory-bank/memory-registry.yaml` 在 `lessons_policy` 下声明 `lesson_schema`。
  - 灵感来源：腾讯程序员《Harness 不是目的，知识才是护城河》一文中 5 类 × 3 级模型；本仓库取最小子集（不引入 5 层存储 / 跨项目知识仓库 / 远程操控）。

- L7 `Lesson 引用追踪闭环（v5.3）`：已固化为 `check_memory_consistency.scan_lesson_refs()` + `--update-refs` 写回模式 + `evolution/lesson-index.json` 三字段（`last_referenced` / `reference_count` / `referenced_in`）。变更点：
  - `evolution/lesson-index.json` schema_version 升 `v5.3`，每条 lesson 加三字段；L1~L6 一次性扫描回填，L7 新增条目。
  - `scripts/check_memory_consistency.py`：扫描 `memory-bank/{progress,activeContext,architecture}.md` + `docs/AI_CHANGELOG.md` + `evolution/promotion-log.md` + `plans/**/*.md`；活跃/Pinned 零引用 WARN；字段漂移 WARN；`--update-refs` merge 写回（保留 v5.2 已有字段）。
  - `docs/LESSONS_RULES.md` 增「引用追踪闭环（v5.3）」章节，定义字段、扫描语料、写法约定、维护命令、checker 行为。
  - `docs/agents/{lessons-policy,evolution-policy}.md` 补引用追踪说明并把 `last_referenced` 引入衰减判定。
  - `memory-bank/memory-registry.yaml` v5.3，`lesson_schema` 增 `tracking_fields` / `scan_targets` / `unused_thresholds_months`；`checks` 增 `update_lesson_refs`。
  - 灵感来源：同一篇文章中"知识仓库需被工作流真实使用才算活"——本次以最小代价（不引入 Git knowledge repo / cross-project sync）只在 lesson-index.json 上加三字段 + 一个 scanner 实现"心跳监测"。
- `docs/agents/*.md` Layer B 摘要：六个细则文档顶部加 ≤8 行的「Layer B 摘要」块（何时该读 / 包含内容 / 不在此处），降低代理首次加载成本。来源：harness-creator 三级渐进索引思想（AGENTS.md=Layer A Map，docs/agents/*=Layer C Reference，Layer B 摘要补在 Reference 顶部）。

## [2026-05-12] promote | L8 日志前缀 + 孤儿守护 linter (v5.4)
- L8 `时间序日志标题前缀与孤儿页面守护（v5.4）`：已固化为 `check_memory_consistency.py` 的 `check_log_prefix()` + `check_orphan_docs()`。变更点：
  - `scripts/check_memory_consistency.py` 新增两个 WARN 级 linter；统一前缀语法常量 `LOG_PREFIX_RE` / `LOG_PREFIX_KINDS` / `LOG_PREFIX_FILES`。
  - `docs/AI_CHANGELOG.md`（6 条）/ `evolution/promotion-log.md`（3 条）/ `memory-bank/progress.md`（2 条）共 11 个历史日期标题改写为 `## [YYYY-MM-DD] <kind> | <summary>`。
  - `docs/LESSONS_RULES.md` 增「时间序日志标题前缀（v5.4）」+「孤儿页面守护（v5.4）」两章节。
  - `evolution/lesson-index.json` schema_version → `v5.4`，新增 L8 条目（type=decision, maturity=verified）。
  - `memory-bank/memory-registry.yaml` v5.4，`lessons_policy` 下新增 `log_prefix` / `orphan_docs` 声明。
  - 灵感来源：Karpathy《LLM Wiki》gist 的 `log.md` 时间线约定 + Lint 操作（contradictions / stale claims / orphan pages / missing cross-refs / data gaps）。本仓库取「parseable log prefix」+「orphan docs」两项最小子集，不引入 contradiction detection / source_hash / sigma-guard。
