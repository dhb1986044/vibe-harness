# AI ChangeLog

## [2026-05-23] changelog | v5.7 默认上下文 profile 与预算门禁
- 范围：`AGENTS.md`、`memory-bank/{memory-registry,activeContext,progress}.md`、`scripts/{context_budget,check_memory_consistency,install_vibe_harness}.py`、`scripts/hooks/codex_session_start.py`、`.github/instructions/governance.instructions.md`、`docs/agents/{memory-model,lifecycle,safety-and-completion,hooks-and-commands,project-modes}.md`、`README_DEPLOYMENT.md`、`docs/LESSONS.md`、`evolution/lesson-index.json`、`evolution/promotion-log.md`。
- 变更：
  - **profile 化读取**：registry 升至 v5.7，新增 `read_policy.default_profile` 与 `light / standard / full`；`full` 保留 v5.6 bootstrap_order 兼容路径。
  - **预算工具**：新增 `scripts/context_budget.py --profile light|standard|full --json`，输出文件/切片清单、字节数、粗略 token、预算状态。
  - **checker 加固**：`check_memory_consistency.py` 校验 profile schema、默认 `light`、`full` 与 legacy bootstrap 等价，并把 light/standard 超预算视为 ERROR。
  - **安装器加固**：`install_vibe_harness.py` 新增 `--context-profile` 与 `--skill-set {lean,full}`；默认 lean 不删除目标既有 skill，full 可复现 v5.6 重治理形态。
  - **SessionStart 降噪**：Codex SessionStart 只提示默认 profile 和 LESSONS 触发条件，不再要求每轮读取完整 LESSONS。
  - **经验沉淀**：新增 L12「默认上下文必须预算化并按需展开」，评估为保留 lesson，不新增 skill。
- 原因：v5.6 默认 bootstrap 约 52KB，普通任务也会支付 full governance 成本；本次把安全能力保留在 full profile，把默认路径降为 light，降低 token 消耗且保持可回滚。
- 风险等级：中。影响代理入口契约、安装结果和 memory checker；通过保留 `bootstrap_order`、`full` profile、旧命令和 WARN-only 旧 registry 兼容降低风险。
- 复杂度影响评分：5/10。
- 验证方式：`python -m py_compile scripts/install_vibe_harness.py scripts/check_memory_consistency.py scripts/context_budget.py scripts/hooks/codex_session_start.py`；`python scripts/context_budget.py --profile light --json`；`python scripts/context_budget.py --profile standard --json`；`python scripts/context_budget.py --profile full --json`；`python scripts/check_memory_consistency.py --strict`；`python scripts/sync_vibe_skills.py --check`；安装器三组 dry-run；Codex SessionStart smoke。
- 回滚方式：`git restore AGENTS.md memory-bank/memory-registry.yaml memory-bank/activeContext.md memory-bank/progress.md scripts/context_budget.py scripts/check_memory_consistency.py scripts/install_vibe_harness.py scripts/hooks/codex_session_start.py .github/instructions/governance.instructions.md docs/agents README_DEPLOYMENT.md docs/LESSONS.md evolution/lesson-index.json evolution/promotion-log.md docs/AI_CHANGELOG.md`，并删除新增 `scripts/context_budget.py` 如需完全回退。
- 关联 lessons：L1 L2 L3 L7 L8 L10 L11 L12。

## [2026-05-22] changelog | platform_design 安装复盘后的 hook 与 Copilot 治理加固
- 范围：`.codex/hooks.json`、`.claude/settings.example.json`、`scripts/{install_vibe_harness,check_memory_consistency,evolve_lessons}.py`、`docs/agents/{hooks-and-commands,project-modes}.md`、`docs/LESSONS.md`、`docs/LESSONS_ARCHIVE.md`、`evolution/lesson-index.json`、`evolution/promotion-log.md`、`evolution/candidates/`、`memory-bank/{activeContext,progress}.md`，并同步修正 `D:/workspace/wl/platform_design` 的安装结果。
- 变更：
  - **跨平台 hook**：Codex hook 命令从 `/usr/bin/env python3 ...` 改为 `python "$(git rev-parse --show-toplevel)/..."`；Claude 示例改为 `python scripts/hooks/memory_stop_guard.py`。
  - **安装器加固**：`install_vibe_harness.py` 跳过 `__pycache__`、`.pyc`、`.git`、`.serena`、虚拟环境和本地缓存；所有模式下补齐缺失的 `.github/instructions/governance.instructions.md` 与 `.claude/settings.json`，但保留目标项目已有配置。
  - **checker 加固**：`check_memory_consistency.py` 新增 Copilot governance instruction 存在性检查，并验证 `applyTo` 覆盖 memory/LESSONS/evolution/vibe skills/hooks/checker 等治理路径。
  - **evolve 写回稳固**：`evolve_lessons.py` 写回 `lesson-index.json` 时将 markdown tags 单元格解析回数组，避免把既有 JSON tags schema 退化成字符串。
  - **目标项目落地**：`platform_design` 补 `.claude/settings.json` 与 `.github/instructions/governance.instructions.md`，收窄原 `spec-driven-workflow-v1.instructions.md` 的 `applyTo` 到 SPEC/ADR/plans/.copilot-tracking，降低与 AGENTS 生命周期的叠加风险。
  - **经验沉淀**：新增 L11「安装后必须实测 agent hook 与 Copilot applyTo」，归档 L4 以保持 active 窗口为 10 条；`evolve_lessons.py --write` 生成 L11 晋升候选。
- 原因：安装到 `platform_design` 后的复盘显示，源仓模板虽然通过 memory check，但目标环境存在“配置看似安装、实际 hook 不触发”和“文档声明 Copilot applyTo、文件缺失”的静默风险。业内实践也要求自动化控制必须能被实际验证，不能只停留在文档约定。
- 风险等级：中。影响安装入口、hook 触发和 Copilot 指令注入；本次保持无新依赖、不覆盖既有目标配置、discovery 阶段仍 warn-only。
- 复杂度影响评分：4/10。
- 验证方式：`python -m py_compile scripts/install_vibe_harness.py scripts/check_memory_consistency.py`；源仓与目标项目 `python scripts/check_memory_consistency.py --strict`；目标项目 `python "$(git rev-parse --show-toplevel)/scripts/hooks/codex_session_start.py"` 与 `codex_stop_memory_guard.py` smoke；`python scripts/sync_vibe_skills.py --check`；安装器 skip 函数正/负例；`python scripts/check_memory_consistency.py --update-refs`。
- 回滚方式：`git restore .codex/hooks.json .claude/settings.example.json scripts/install_vibe_harness.py scripts/check_memory_consistency.py docs/agents/hooks-and-commands.md docs/agents/project-modes.md docs/LESSONS.md docs/LESSONS_ARCHIVE.md evolution/lesson-index.json evolution/promotion-log.md memory-bank/activeContext.md memory-bank/progress.md`；目标项目对应路径用 `git -C D:/workspace/wl/platform_design restore <path>` 回滚，新增 `.claude/settings.json` / `.github/instructions/governance.instructions.md` / L11 candidate 如需移除须先确认删除。
- 关联 lessons：L1 L2 L7 L8 L9 L10 L11。

## [2026-05-22] changelog | 首次 Git 发布准备
- 范围：`.gitignore`、`.gitattributes`、`plans/commit-plan.md`、`memory-bank/activeContext.md`、`memory-bank/progress.md`、`docs/AI_CHANGELOG.md`。
- 变更：
  - 新增根 `.gitignore`，排除 Python 缓存、`.serena/` 本地工具状态、环境文件和 OS/editor 噪声，避免首次提交混入运行时产物。
  - 新增 `.gitattributes`，统一文本文件 LF，避免 Windows `core.autocrlf` 造成后续跨平台换行漂移。
  - 新增 `plans/commit-plan.md`，记录首次提交的范围、命令、检查项、风险和回滚策略。
  - 刷新 `activeContext.md` 与 `progress.md`，把当前焦点切换为首次 Git 发布任务。
- 原因：当前目录不是 Git 工作树，用户要求提交并推送到 GitHub；按 `vibe-git` 契约，提交前需要明确计划、同步 memory 并确保提交范围可解释。
- 风险等级：中。首次推送会把当前目录发布到远端仓库；本次只做发布准备，不改业务逻辑或治理脚本行为。
- 复杂度影响评分：1/10。
- 验证方式：`python scripts/check_memory_consistency.py --strict`；敏感词扫描；Python 语法检查；`git diff --cached --check`；`git push -u origin main` 成功；`git ls-remote --heads origin main` 返回远端 `main` 指向 `5a8bc5c1386367fa266b8ced6d51baa73943d564`。
- 回滚方式：提交前删除本地 `.git/` 或移除新增治理文件；提交后但推送前可用 `git reset --soft HEAD~1`；推送后优先追加修正提交，不做强制覆盖。
- 关联 lessons：L1 L2 L7 L8 L10。

## [2026-05-19] changelog | evolve 写回 merge + PreTool 危险命令加固
- 范围：`scripts/evolve_lessons.py`、`scripts/hooks/codex_pre_tool_guard.py`、`docs/AI_CHANGELOG.md`、`memory-bank/progress.md`、`memory-bank/activeContext.md`、`evolution/lesson-index.json`（lesson 引用回填）。
- 变更：
  - **`evolve_lessons.py` schema-safe 写回**：`parse_index()` 支持当前 `docs/LESSONS.md` 7 列索引，同时保留 5 列兼容；`--write` 不再重建整个 `lesson-index.json`，改为按 lesson id merge 既有对象，保留 `schema_version`、`type`、`maturity`、`last_referenced`、`reference_count`、`referenced_in`、历史 `promotion_status` / `promotion_target` 及未知字段；只更新标题、标签、优先级、状态、promotion score/source 等脚本拥有的派生字段；promotion-log 新标题改为 `## [YYYY-MM-DD] promote | ...`。
  - **UTF-8 BOM 兼容**：读取 `docs/LESSONS.md` 与 `evolution/lesson-index.json` 时使用 `utf-8-sig`，兼容 PowerShell / Windows 工具生成的带 BOM UTF-8 文件。
  - **`codex_pre_tool_guard.py` 跨平台危险命令拦截**：保持无依赖正则策略和现有 hook 输出接口，扩展拦截 `git reset --hard`、`git clean -fdx/-dfx`、强制 push、Linux 根目录递归删除、PowerShell `Remove-Item -Recurse -Force`、Windows `rmdir /s /q` / `del /s /q`。
  - **治理记录同步**：刷新 `progress.md` 与 `activeContext.md`；不新增 LESSON，本次属于 L6/L7/L8/L10 的落地修复，并遵守 L1/L2 的命令与门禁要求。
- 原因：`memory-bank/activeContext.md` 与历史 progress 已明确记录 `evolve_lessons.py --write` 仍是 v5 schema 硬编码，会覆盖 v5.2+ lesson 元数据；研究报告也建议强化简单、可验证、可回滚的治理脚本与危险命令门禁。本次取最小修复，不引入新 skill、外部依赖或复杂框架。
- 风险等级：中。`evolve_lessons.py` 涉及治理索引写回，`codex_pre_tool_guard.py` 涉及命令阻断行为；实现保持保守 merge 与高风险组合匹配，避免扩大为通用命令策略引擎。
- 复杂度影响评分：3/10。
- 验证方式：`python -m py_compile scripts/evolve_lessons.py scripts/hooks/codex_pre_tool_guard.py`；`PYTHONIOENCODING=utf-8 python scripts/evolve_lessons.py` dry-run；临时目录 `--write` merge smoke 验证 schema 与未知字段不丢失；hook 正负例 stdin 测试；`python scripts/check_memory_consistency.py --update-refs`；`python scripts/check_memory_consistency.py --strict`。
- 回滚方式：当前目录未检测到 `.git`；如在 git 仓库中回滚，可执行 `git restore scripts/evolve_lessons.py scripts/hooks/codex_pre_tool_guard.py docs/AI_CHANGELOG.md memory-bank/progress.md memory-bank/activeContext.md evolution/lesson-index.json`。无 git 时按上述文件从备份或上一版本恢复。
- 关联 lessons：L1 L2 L6 L7 L8 L10。

## [2026-05-19] changelog | v5.6 项目模式 + phase 切档 + 入口 skill
- 范围：`memory-bank/memory-registry.yaml`、`scripts/check_memory_consistency.py`、`scripts/hooks/{memory_stop_guard,codex_stop_memory_guard}.py`、`scripts/install_vibe_harness.py`、`scripts/discover_project.py`（新增）、`AGENTS.md`、`docs/agents/project-modes.md`（新增）、`docs/agents/onboarding/`（新增 9 份手册 + README）、`.claude/skills/{vibe-bootstrap,vibe-retrofit,vibe-discovery,vibe-exec}/`（新增）、`.codex/skills/{vibe-bootstrap,vibe-retrofit,vibe-discovery,vibe-exec}/`（新增）、`.claude/skills/_legacy/README.md`（新增）、`.codex/skills/_legacy/README.md`（新增）、`docs/LESSONS.md`、`evolution/lesson-index.json`。
- 变更：
  - **项目模式建模**：registry 顶层引入 `project_mode ∈ {new_project, vibe_managed_legacy, unmanaged_legacy}` 与 `harness_phase ∈ {discovery_only, shadow_harness, soft_gate, managed_harness}`；集中声明 `governance_paths` 与 `hook_policy`。本仓库自身声明为 `vibe_managed_legacy + managed_harness`。
  - **phase-aware check**：`check_memory_consistency.py` 加 `PROJECT_MODES` / `HARNESS_PHASES` 常量、`parse_registry_phase()`、`--print-phase`、`--warn-only` 三件套；discovery/shadow 阶段所有 errors 自动降级为 warnings；PASS/FAIL 输出附带 `[mode=... phase=...]` 标签。
  - **phase-aware hooks**：`memory_stop_guard.py` / `codex_stop_memory_guard.py` 重写为：先 `--print-phase` 读阶段，warn-only 阶段安静退出；`soft_gate` 仅当错误命中 `governance_paths` 才 block；`managed_harness` 维持旧的"任失败即 block"。
  - **入口 skill 四件套**：`.claude/skills/` 与 `.codex/skills/` 各新增 `vibe-bootstrap` / `vibe-retrofit` / `vibe-discovery` / `vibe-exec`。**显式不进 `sync_vibe_skills.py` 三向镜像**，两端独立演进；Copilot 经 AGENTS.md §1.1 + `docs/agents/project-modes.md` 跳转，不在 `.github/skills/` 复制。
  - **AGENTS.md**：§1 新增 §1.1 "三类项目模式（v5.6）"小节，给出模式表 + phase 四档；§12 skill 索引新增"入口 skill"段（含不镜像声明）。
  - **discover_project.py**：从 v5.1 移植的只读侦察脚本，产出 `PROJECT_DISCOVERY_REPORT.md` 与 `memory-bank/*.draft.md`。
  - **install_vibe_harness.py 加固**：重写为支持 `--mode {bootstrap, retrofit, discovery}`、`--dry-run`、`--overwrite-agents`；`is_map_agents()` 识别 v5.5+ Map 结构，retrofit 默认写 `AGENTS.v5.6.draft.md` 而非覆盖。
  - **onboarding 手册**：从 v5.1 平移 9 份 `manuals/*.md` 到 `docs/agents/onboarding/`，加 README 索引。
  - **legacy 通道**：`.claude/skills/_legacy/` 与 `.codex/skills/_legacy/` 增 README 占位说明（本仓库自身无 legacy skill）。
  - 新增 lesson L10（decision/verified）。
- 原因：来自三方架构评估 + v5.1 兄弟目录的"项目模式 / phase 切档 / 入口 skill"概念与 v5.5 的"Map AGENTS + 三向同步 + lesson schema"正交且互补；硬切 managed_harness 接入历史项目会触发误报阻塞，需要 discovery → shadow → soft_gate → managed 的渐进档位。本次集成在保持 v5.5 治理面不变前提下叠加 v5.1 的接入策略层。
- 风险等级：中。Hook 行为改变是最敏感点；但本仓库自身处于 managed_harness，行为与 v5.5 完全一致（PASS 路径不变）；warn-only / soft_gate 路径只在显式声明的 phase 下触发。
- 验证方式：`python scripts/check_memory_consistency.py --strict` PASS（mode=vibe_managed_legacy phase=managed_harness）；`--print-phase` 输出符合预期；`sync_vibe_skills.py --check` 仍 PASS（治理四件套未被入口 skill 影响）；`install_vibe_harness.py --dry-run` 与 `discover_project.py` 烟雾测试通过；两个 stop hook 直跑均退出 0。
- 回滚方式：`git restore` 上述全部路径；删除新增的 `.claude/skills/{vibe-bootstrap,vibe-retrofit,vibe-discovery,vibe-exec}/`、`.codex/skills/{...}`、`docs/agents/onboarding/`、`docs/agents/project-modes.md`、`scripts/discover_project.py`。
- 关联 lessons：L1 L2 L3 L9 L10。

## [2026-05-12] changelog | v5.5 Copilot 集成 + 三向同步
- 范围：`scripts/sync_vibe_skills.py`、`scripts/check_memory_consistency.py`、`AGENTS.md`、`.github/copilot-instructions.md`、`.github/instructions/governance.instructions.md`（新增）、`.github/skills/vibe-{memory-check,guard,xcheck,evolve}/`（新增镜像）、`docs/agents/hooks-and-commands.md`、`memory-bank/memory-registry.yaml`、`docs/LESSONS.md`、`evolution/lesson-index.json`、`evolution/promotion-log.md`、`memory-bank/progress.md`、`memory-bank/activeContext.md`。
- 变更：
  - 同步器升级为三向：`MIRRORS = {codex: .codex/skills, copilot: .github/skills}`；新增 `diff_one()` / `_write_mirror()`；保留 `diff()` 并集聚合器作向后兼容 API；`docs/` 子目录通过 backup-restore 允许三端分歧。
  - `check_memory_consistency.py` 把 `VIBE_SKILLS_MIRROR` 扩展为 `VIBE_SKILLS_MIRRORS = (.codex/skills, .github/skills)`，所有 vibe-* 检查遍历每个镜像。
  - `.github/copilot-instructions.md` 重写为指向 AGENTS.md 的指针 + Copilot 特定约束（无 shell hook → 主动调用 `--strict`；`/memories/repo/` 禁用；`/memories/session/` 与 `/memories/` 允许；三向同步要求）。
  - 新增 `.github/instructions/governance.instructions.md`，通过 `applyTo` 在 memory-bank / LESSONS / evolution / vibe-* / hooks 等治理路径被动注入 MEMORY_CHECK / 三向同步 / 引用回填提醒。
  - `AGENTS.md` §9 MEMORY_CHECK 触发列表增加 `.github/skills/vibe-*/**`、`.github/instructions/**`、`.github/copilot-instructions.md`；§10 加 Copilot 三层兜底子节；§11 加 Copilot 完成清单脚注；§12 触发面与单源策略加入 `.github/skills/`。
  - `docs/agents/hooks-and-commands.md` 加 Copilot 章节（无 shell hook → applyTo + 自律）。
  - `memory-bank/memory-registry.yaml` 升至 v5.5：`skill_roots.copilot: .github/skills`；新增 `agent_targets` 块（含 `memory_policy.repo_scope_forbidden: true`）。
  - 新增 lesson L9（decision/verified）。
- 验证：`python scripts/sync_vibe_skills.py --check` PASS（codex + copilot 两路均同步）；`python scripts/check_memory_consistency.py --strict` PASS。

## [2026-05-12] changelog | v5.4 日志前缀标准化 + 孤儿页面 linter
- 范围：`scripts/check_memory_consistency.py`、`docs/AI_CHANGELOG.md`、`evolution/promotion-log.md`、`memory-bank/progress.md`、`docs/LESSONS.md`、`docs/LESSONS_RULES.md`、`evolution/lesson-index.json`、`memory-bank/memory-registry.yaml`、`memory-bank/activeContext.md`。
- 变更：
  - **`scripts/check_memory_consistency.py`**：新增 `check_log_prefix()`（强制 `## [YYYY-MM-DD] <kind> | <summary>` 格式，kind ∈ `{changelog, promote, lint, progress, evolve, ingest, decision}`）；新增 `check_orphan_docs()`（两向绑定：`docs/agents/*.md` 必须被 `AGENTS.md` 引用，`memory-bank/*.md` 必须被 `memory-registry.yaml` 列出）。两者均 WARN 级，不阻塞 `--strict` 退出码。
  - **历史标题迁移**：`AI_CHANGELOG.md` 6 条 + `promotion-log.md` 3 条 + `progress.md` 2 条，共 11 个 `## YYYY-MM-DD (...)` 标题改写为新格式，使 `grep "^## \[" <file> | tail -5` 稳定可用。
  - **`LESSONS_RULES.md`**：增「时间序日志标题前缀（v5.4）」+「孤儿页面守护（v5.4）」两章节。
  - **`LESSONS.md`**：活跃窗口扩为 `L1-L8`，新增 L8 (decision/verified)。
  - **`lesson-index.json`**：`schema_version` → `v5.4`，新增 L8 条目。
  - **`memory-registry.yaml`**：版本 → `v5.4`，`lessons_policy` 下新增 `log_prefix.{files,pattern,kinds}` + `orphan_docs.catalog_pairs` 声明。
- 原因：v5.3 给 lesson 装上了"心跳监测"，但仓库内的时间序产物（CHANGELOG / promotion-log / progress）格式不统一，`grep` 难以稳定抽取时间线；`docs/agents/*.md` 与 `memory-bank/*.md` 缺与 catalog 的反向守护，新增孤儿文件无门禁。对照 Karpathy《LLM Wiki》gist 的 log.md 约定与 Lint 操作（contradictions / stale claims / orphan pages / missing cross-refs / data gaps）取最小子集落地。
- 风险等级：低。两个新 linter 均 WARN 级、向后兼容；只触碰已迁移条目的标题行；不修改任何 lesson 业务字段；不引入新依赖。
- 验证方式：`python scripts/check_memory_consistency.py --strict` PASS 无 log-prefix / orphan WARN；`--update-refs` 后再次 `--strict` 无引用漂移 WARN。
- 回滚方式：`git restore scripts/check_memory_consistency.py docs/AI_CHANGELOG.md docs/LESSONS.md docs/LESSONS_RULES.md evolution/lesson-index.json evolution/promotion-log.md memory-bank/memory-registry.yaml memory-bank/progress.md memory-bank/activeContext.md`。
- 关联 lessons：L1 L3 L6 L7 L8。

## [2026-05-12] changelog | lesson 引用追踪闭环 v5.3 + docs/agents Layer B 摘要
- 范围：`scripts/check_memory_consistency.py`、`evolution/lesson-index.json`、`docs/LESSONS.md`、`docs/LESSONS_RULES.md`、`docs/agents/{lessons-policy,evolution-policy,lifecycle,memory-model,safety-and-completion,hooks-and-commands}.md`、`memory-bank/memory-registry.yaml`、`evolution/promotion-log.md`、`memory-bank/progress.md`、`memory-bank/activeContext.md`。
- 变更：
  - **引用追踪闭环（L7）**：在 `evolution/lesson-index.json` 每条 lesson 上新增三字段 `last_referenced` / `reference_count` / `referenced_in`；`schema_version` 升至 `v5.3`。
  - **`scripts/check_memory_consistency.py`**：
    - 新增 `scan_lesson_refs(known_ids)`：扫描 `memory-bank/progress.md`、`activeContext.md`、`architecture.md`、`docs/AI_CHANGELOG.md`、`evolution/promotion-log.md`、`plans/*.md`、`plans/**/*.md`，匹配裸 `L\d+` 提及，按文件内最近 ISO 日期就近归属。
    - `check()` 内新增对比逻辑：活跃 / Pinned lesson 在扫描语料中零引用 → WARN「建议归档或在下个任务中验证」；JSON 中 `last_referenced` / `reference_count` 与扫描结果漂移 → WARN「运行 `--update-refs` 刷新」。
    - 新增 `--update-refs` CLI 模式：merge 写回三字段，保留 `type` / `maturity` / `promotion_status` 等所有其他字段，避免 v5.2 schema 被覆盖。
  - **`LESSONS_RULES.md`**：新增「引用追踪闭环（v5.3）」章节，定义字段、扫描语料、写法约定、维护命令与 checker 行为。
  - **`evolution-policy.md`**：新增「引用频次作为衰减信号」章节，把 `last_referenced` 引入衰减判定。
  - **`lessons-policy.md`**：新增简短引用追踪说明，回链至 `LESSONS_RULES.md`。
  - **`memory-registry.yaml`**：版本 → `v5.3`；`lesson_schema` 增 `tracking_fields` / `scan_targets` / `unused_thresholds_months`；`checks` 增 `update_lesson_refs`。
  - **L7 入 `LESSONS.md` 与 `lesson-index.json`**：记录本次 process 类 lesson 本身。
  - **`docs/agents/*.md` Layer B 摘要**：六个细则文档（`lifecycle` / `memory-model` / `lessons-policy` / `evolution-policy` / `safety-and-completion` / `hooks-and-commands`）顶部新增 ≤8 行的「Layer B 摘要」块（何时该读 / 包含内容 / 不在此处），降低代理首次加载成本与决定是否展开的判断成本。
- 原因：v5.2 给 lesson 装上了 type + maturity 元数据，但活跃窗口是否被工作流真实"使用"——是否在 PLAN/EXEC/CHANGELOG 等产物中被引用——没有任何信号。零引用即衰减信号；这是 LESSONS L7 想要落地的本质。同时 v5.1 把 AGENTS.md 拆为 Map + Reference 之后，细则文档缺 Layer B（分类清单 + 何时该读），代理点开任一篇都得读完整段才能判断是否相关。
- 风险等级：低。新增字段都是可选/可选位置；scanner 行为是只读 + WARN，不影响 `--strict` 退出码（除非 schema 漂移升级为 error，目前不升级）；`--update-refs` 是 merge 模式，与 v5.2 schema 兼容；Layer B 摘要只在文件头追加块，不改既有正文。
- 验证方式：`python scripts/check_memory_consistency.py --strict` PASS；运行 `python scripts/check_memory_consistency.py --update-refs` 后再次 `--strict` 无引用漂移 WARN。
- 回滚方式：`git restore scripts/check_memory_consistency.py evolution/lesson-index.json docs/LESSONS.md docs/LESSONS_RULES.md docs/agents/ memory-bank/memory-registry.yaml docs/AI_CHANGELOG.md evolution/promotion-log.md memory-bank/progress.md memory-bank/activeContext.md`。
- 关联 lessons：L1 L3 L6 L7。

## [2026-05-12] changelog | lesson schema v5.2 (type + maturity)
- 范围：`docs/LESSONS.md`、`docs/LESSONS_RULES.md`、`evolution/lesson-index.json`、`evolution/promotion-log.md`、`scripts/check_memory_consistency.py`、`docs/agents/evolution-policy.md`、`memory-bank/memory-registry.yaml`。
- 变更：
  - **Schema 扩展**：每条 lesson 新增两个结构化字段 `type ∈ {model, decision, guideline, pitfall, process}` 与 `maturity ∈ {draft, verified, proven}`。这是对腾讯程序员《Harness 不是目的，知识才是护城河》一文中 5 类 MECE × 3 级成熟度模型的最小子集采纳——不引入 5 层存储分层、不引入独立 Git 知识仓库、不引入跨设备远程操控，只在现有 LESSONS 体系上加这 2 个字段。
  - **`LESSONS_RULES.md`**：定义 type 5 类含义与示例、maturity 3 级进入条件与衰减建议；正文模板增加两行字段；索引列定义改为 7 列。
  - **`LESSONS.md`**：索引扩为 7 列（`#`、`标题`、`类型`、`成熟度`、`标签`、`优先级`、`状态`）；L1~L5 正文与索引按现状回填字段；新增 L6 记录本次 schema 演进本身。
  - **`evolution/lesson-index.json`**：`schema_version` 从 `v5` → `v5.2`；每条 lesson 增加 `type` 与 `maturity` 字段；L6 同步入索引。
  - **`scripts/check_memory_consistency.py`**：
    - 重写 `parse_lessons_index()` 支持 7 列新格式 + 5 列向后兼容（按表头列名映射，缺列降级为空字符串）。
    - 新增 `parse_lesson_bodies()` 解析 `## L{n}` 段落里的 `- 类型：` / `- 成熟度：` 字段。
    - 在 `check()` 中加 lesson-schema lint：active/Pinned 缺 `类型`/`成熟度` → ERROR（WHAT+WHY+HOW 三段式）；type/maturity 取值不在白名单 → ERROR；索引与正文漂移 → ERROR；索引与 lesson-index.json 漂移 → ERROR；正文缺字段（但索引有）→ WARN；活跃窗口 draft 数量 > 5 → WARN（信号稀释保护）。
    - JSON 校验同步扩展：lesson-index.json 缺 type/maturity → WARN；非法取值 → ERROR；与 markdown 索引漂移 → ERROR。
  - **`evolution-policy.md`**：升级判断新增"Maturity 作为晋升锚点"与"Type 作为晋升路径选择"两节；draft 不进入晋升候选；verified 进入；proven 须填具体载体；衰减建议表给出 12/6 月阈值。
  - **`memory-registry.yaml`**：版本升 `v5.2`；`lessons_policy` 下新增 `lesson_schema` 子键，声明 `required_fields / types / maturities / draft_soft_limit_in_active_window`。
- 原因：原 LESSONS 体系只有 `status` 与 `priority` 两个粗粒度信号，导致 (1) `vibe-evolve` 晋升判定只能依赖 frequency/severity，无法体现"经验是否经过验证"；(2) 没有衰减锚点，活跃窗口长期会堆积过时 lesson；(3) 缺乏类型分类，晋升路径选择只能凭直觉。本次以最小代价（不改 skill、不引入新仓库）补齐元数据 schema，为后续按需引入"引用追踪闭环"和"跨项目知识源"打基础。
- 风险等级：低。纯文档/脚本元数据扩展，向后兼容旧 5 列索引解析（仅会触发字段缺失 ERROR，提示用户补齐）；现有 lesson 已全部回填到合理 type+maturity；linter 错误信息符合 v5.1 WHAT+WHY+HOW 三段式标准。
- 验证方式：`python scripts/check_memory_consistency.py --strict` PASS。
- 回滚方式：`git restore docs/LESSONS.md docs/LESSONS_RULES.md docs/agents/evolution-policy.md docs/AI_CHANGELOG.md evolution/lesson-index.json evolution/promotion-log.md scripts/check_memory_consistency.py memory-bank/memory-registry.yaml`。

## [2026-05-07] changelog | skill 三层一致性整治 + ghost-file linter
- 范围：`.codex/skills/vibe-{knowledge,context,debug,review,xcheck,pipeline,changelog}/`、`docs/agents/memory-model.md`、`scripts/check_memory_consistency.py`、`evolution/promotion-log.md`、`docs/LESSONS.md`、`evolution/lesson-index.json`。
- 变更：
  - **Phase 1 frontmatter 修正**：`vibe-knowledge/SKILL.md` 与 `vibe-context/SKILL.md` 的 `description` 字段与正文冲突（前者写 PROJECT_GUIDE.md 但正文禁止；后者写 briefing/open_questions 但正文禁止），已对齐为 `architecture.md / docs/LESSONS.md` 与 `activeContext.md`。
  - **Phase 2 docs/ 幽灵引用清理**：13 个 .codex/skills/vibe-*/docs/*.md 文件中（涉及 vibe-context、vibe-debug、vibe-knowledge、vibe-review、vibe-xcheck、vibe-pipeline）残留的 PROJECT_GUIDE / briefing.md / open_questions.md 引用全部清除。
  - **Phase 3 promotion-log 补全**：补上 L3 的固化记录（v5.1 模板 + sync_vibe_skills + L2 引用检查）与 L4 的候选状态。
  - **Phase 3 vibe-changelog 何时不用**：补"跳过条件"段（纯注释/typo/格式化/.gitignore/CHANGELOG 自身修订）。
  - **Phase 4 触发矩阵澄清**：vibe-omega 加注"EXEC 后审计 + v2 计划生成（不是 EXEC 执行器）"；vibe-plan vs vibe-alpha 加决策提示。
  - **Phase 5 ghost-file linter（核心产出）**：在 `check_memory_consistency.py` 的 `check_referenced_paths()` 加第 6 项检查，扫描 `.claude/skills/` 与 `.codex/skills/` 全部 SKILL.md + docs/*.md，禁止出现 `PROJECT_GUIDE` / `briefing.md` / `open_questions.md` 三个幽灵符号，但允许在否定语境（"不创建"、"未注册"、"deprecated" 等）中合法出现。
  - **Phase 6 沉淀**：新增 LESSONS L5「Skill 三层一致性：description / SKILL.md 正文 / docs/」，候选直接晋升为 P1 active 并标记 promoted:ghost-file-linter；同步 lesson-index.json。
- 原因：上一轮（2026-05-07 skill cleanup）只解决了"调用不存在脚本/写入未注册文件"的部分，遗留 frontmatter 与 docs/ 子目录大量幽灵引用。本轮发现的新规律是"skill 自我矛盾"，必须用 linter 而非人工巡查防止回潮。
- 风险等级：低（纯文档清理 + 增加门禁，不改变任何运行时行为；linter 误判通过否定语境豁免兜底）。
- 验证方式：`python scripts/sync_vibe_skills.py --check` PASS；`python scripts/check_memory_consistency.py --strict` PASS（含新加的 ghost-file 检查）；`grep -r "PROJECT_GUIDE\|briefing\.md\|open_questions\.md" .codex/.claude/` 仅剩否定语境合法行。
- 回滚方式：`git restore .codex/skills/ scripts/check_memory_consistency.py docs/agents/memory-model.md docs/AI_CHANGELOG.md docs/LESSONS.md evolution/lesson-index.json evolution/promotion-log.md`。

## [2026-05-07] changelog | skill cleanup
- 范围：`.codex/skills/`、`AGENTS.md` §12、`docs/agents/memory-model.md`、`scripts/sync_vibe_skills.py`、`docs/LESSONS.md`、`evolution/lesson-index.json`。
- 变更：
  - 删除 4 个错位 skill：`vibe-prompt`、`vibe-data`、`vibe-parallel`、`vibe-knowledge-modifier`（业务专属或与 harness 通用治理目标不匹配；后者还引用了不存在的 `evolution_analysis_*.md`）。
  - 修正 `vibe-review/SKILL.md`：移除硬编码 L2-L9 引用（来自 badcase-miner 项目），改为读取本项目 `docs/LESSONS.md` 实际命中的编号。
  - 修正 `vibe-changelog/SKILL.md`：移除不存在的 `python scripts/log_change.py` 调用，改为按模板 markdown 追加。
  - 修正 `vibe-knowledge/SKILL.md`：路径从 `PROJECT_GUIDE.md` 改为 memory-bank 已注册文件（`architecture.md` ADR / `LESSONS.md`）。
  - 修正 `vibe-context/SKILL.md`：取消创建未注册的 `briefing.md` / `open_questions.md`，改为追加到 `activeContext.md`。
  - 修正 `vibe-debug/SKILL.md`：落盘路径从 PROJECT_GUIDE 改为 `progress.md` + 调用 `vibe-lessons`。
  - 补 boundary：`vibe-plan` 与 `vibe-alpha` 的边界、`vibe-pipeline` runbook 显式调用治理四件套、`vibe-lessons` 与 `vibe-evolve` 的职责切分。
  - 清理 stale 引用：`AGENTS.md` §12 排除清单、`memory-model.md` 触发矩阵、`sync_vibe_skills.py` 注释中的 4 个已删 skill 名。
  - 新增 `docs/LESSONS.md` L4：harness 模板不应打包业务专属 skill。
- 原因：审计发现 16 个 codex-only skill 中存在硬编码他项目教训、调用不存在脚本、写入未注册文件、引用业务专属附件等多类一致性缺陷，违反"代理改变仓库状态前必须满足真实事实"。
- 风险等级：中（删除 4 个 skill 不可被引用；已通过 grep 确认仓库内除自身 docs 外无其他引用）。
- 验证方式：`python scripts/sync_vibe_skills.py --check` PASS；`python scripts/check_memory_consistency.py --strict` PASS；grep `vibe-prompt|vibe-data|vibe-parallel|vibe-knowledge-modifier` 仅剩允许的历史/legacy 上下文。
- 回滚方式：`git restore .codex/skills/ AGENTS.md docs/agents/memory-model.md scripts/sync_vibe_skills.py docs/LESSONS.md docs/AI_CHANGELOG.md evolution/lesson-index.json`。

## [2026-05-06] changelog | v5.1 AGENTS.md Map 拆分
- 范围：AGENTS.md、docs/agents/、scripts/、.codex/skills/、.github/skills/using-agent-skills/。
- 变更：
  - AGENTS.md 由 ~350 行 Manual 拆为 127 行 Map + 6 个 docs/agents/ 子文档（lifecycle / memory-model / lessons-policy / evolution-policy / safety-and-completion / hooks-and-commands）。
  - 新增 `scripts/sync_vibe_skills.py`，确立 `.claude/skills/vibe-*` 单源、`.codex/skills/vibe-*` 镜像策略。
  - 扩展 `scripts/check_memory_consistency.py`：新增 L2 引用一致性检查（AGENTS 子文档存在性、vibe-* 镜像同步、SKILL.md 与 registry 引用脚本的存在性），错误信息按 WHAT+WHY+HOW 三段式输出。
  - `using-agent-skills` 决策树新增 `Governance (vibe-*)` 分支。
  - 保留旧版 `AGENTS.legacy.md` 作为回滚锚点。
- 原因：参照 `harness-creator` 的 Map+并行+可操作错误三大原则，对治理闭环做最小升级，不替换 vibe 治理体系。
- 风险等级：中（影响所有代理的 bootstrap 行为）。
- 验证方式：6 项 XCHECK（正向 / 边界（移走镜像）/ 负面（破坏 registry）/ 回归 / AGENTS.md 体积 / 链接活性）全部通过。
- 回滚方式：`Copy-Item AGENTS.legacy.md AGENTS.md -Force`；删除 `docs/agents/`、`scripts/sync_vibe_skills.py`；revert `scripts/check_memory_consistency.py` 中 v5.1 标记的代码块。

## [2026-05-06] changelog | v5 初始骨架
- 范围：vibe-harness-v5 模板。
- 变更：初始化 AGENTS.md v5、memory registry、lesson index、Codex/Claude hooks、vibe skills 和一致性检查脚本。
- 原因：形成可复用的 Agent Harness 自进化模板。
- 风险等级：低
- 验证方式：执行 `python scripts/check_memory_consistency.py --strict`。
- 回滚方式：移除本模板新增文件，恢复原 AGENTS.md 与原 memory 文档。
