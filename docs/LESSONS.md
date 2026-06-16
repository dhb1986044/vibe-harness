# Lessons

## Active Summary
- 默认读取范围：按 `read_policy.default_profile` 读取；`full` 才读取 `Pinned` 条目 + 最近 `5~10` 条 `活跃` 条目
- 当前 `Pinned`：L1
- 当前活跃窗口：`L1-L3, L5-L12`
- 归档库：`docs/LESSONS_ARCHIVE.md`
- 规则说明：`docs/LESSONS_RULES.md`
- 字段约定（v5.2+）：每条 lesson 必须带 `类型(type)` 与 `成熟度(maturity)`，定义见 `LESSONS_RULES.md`。
- 引用追踪（v5.3+）：在工作流产物中以裸 `L\d+` 引用 lesson，`scripts/check_memory_consistency.py --update-refs` 会回写 `last_referenced` / `reference_count` / `referenced_in` 至 `evolution/lesson-index.json`。

## 索引

| # | 标题 | 类型 | 成熟度 | 标签 | 优先级 | 状态 |
|---|---|---|---|---|---|---|
| L1 | 不发明命令 | guideline | proven | [Process,Command] | P1 | Pinned |
| L2 | Memory check 失败不得完成 | process | proven | [Memory,Guard] | P1 | 活跃 |
| L3 | AGENTS.md 是 Map 不是 Manual | decision | proven | [AGENTS,Architecture] | P2 | 活跃 |
| L4 | harness 模板不应打包业务专属 skill | guideline | verified | [Skills,Architecture] | P2 | 已归档 |
| L5 | Skill 三层一致性（description / SKILL.md / docs/） | pitfall | proven | [Skills,Lint] | P1 | 活跃 |
| L6 | Lesson 需带 type+maturity 字段 | decision | verified | [Lessons,Schema] | P2 | 活跃 |
| L7 | Lesson 引用追踪闭环（v5.3） | process | verified | [Lessons,Tracking] | P2 | 活跃 |
| L8 | 时间序日志标题前缀与孤儿页面守护（v5.4） | decision | verified | [Lint,Logs,Docs] | P2 | 活跃 |
| L9 | Copilot 集成与三向同步（v5.5） | decision | verified | [Agents,Integration,Copilot] | P2 | 活跃 |
| L10 | 项目模式与 phase 切档（v5.6） | decision | verified | [Onboarding,Phases,Hooks] | P2 | 活跃 |
| L11 | 安装后必须实测 agent hook 与 Copilot applyTo | pitfall | verified | [Hooks,Copilot,Install] | P1 | 活跃 |
| L12 | 默认上下文必须预算化并按需展开 | decision | verified | [Context,Tokens,Process] | P1 | 活跃 |

## Active Lessons

## L1 不发明命令
- 类型：guideline
- 成熟度：proven
- 场景：代理需要运行、构建、测试或发布项目。
- 风险：凭空编造命令会制造虚假验证，甚至破坏环境。
- 修复策略：先从 README、Makefile、package.json、pyproject.toml、CI、scripts 中发现真实命令。
- 可复用模式：命令发现优先于命令生成。
- 建议升级为 Guard/XCheck/Skill 规则：保留为全局 Guard。

## L2 Memory check 失败不得完成
- 类型：process
- 成熟度：proven
- 场景：任务修改了 `memory-bank`、`docs/LESSONS.md`、`evolution` 或 vibe skills。
- 风险：经验库、索引和 AGENTS 契约漂移，导致后续代理读取错误知识。
- 修复策略：任务结束前执行 `python scripts/check_memory_consistency.py --strict`。
- 可复用模式：memory consistency 是 COMPLETE 前门禁，不是用户手动工具。
- 建议升级为 Guard/XCheck/Skill 规则：已固化为 `vibe-memory-check`。

## L3 AGENTS.md 是 Map 不是 Manual
- 类型：decision
- 成熟度：proven
- 场景：v5 期间 AGENTS.md 累计到 ~350 行，承载契约 + 详细生命周期 + 全部策略，代理首次加载成本高且修改任意一节都触发整文件 diff。
- 风险：（1）超长契约稀释代理注意力，关键门禁规则被忽略；（2）双份维护（.claude vs .codex 治理 skill）漂移；（3）文档间引用路径无 linter 守护，重命名/删除会导致静默失效。
- 修复策略：参照 `harness-creator` 的 "AGENTS.md is a Map, Not a Manual" 原则，将 AGENTS.md 控制在 ~120 行只做导航 + 核心契约骨架，详细内容下沉到 `docs/agents/*.md`；vibe-* 改为单源 + 镜像；扩展 `check_memory_consistency.py` 增加 L2 引用一致性检查（错误信息 WHAT+WHY+HOW 三段式）。
- 可复用模式：契约文件应当是 Map（导航）；策略详情应当是 Reference（按需读取）；文档间引用必须有自动化 linter 守护。
- 建议升级为 Guard/XCheck/Skill 规则：已固化为 v5.1 AGENTS.md 模板 + `scripts/sync_vibe_skills.py` + `check_memory_consistency.check_referenced_paths()`。

## L5 Skill 三层一致性（description / SKILL.md 正文 / docs/）
- 类型：pitfall
- 成熟度：proven
- 场景：二轮审计发现 `vibe-knowledge/SKILL.md` 的 frontmatter `description` 写"写入 PROJECT_GUIDE.md"但正文明确禁止创建该文件；`vibe-context/SKILL.md` 同类（description 写生成 briefing/open_questions 但正文禁止）；并且 7 个 skill 的 docs/ 子目录从 harness-creator 复制过来的模板都保留了这些幽灵引用。
- 风险：（1）frontmatter 是代理选择 skill 的主要依据，与正文冲突会导致 skill 会被错触发或被调用后反退；（2）docs/ 残留幽灵会在代理展开阅读时误导为合法写入路径；（3）人工巡查不可持续。
- 修复策略：在 `scripts/check_memory_consistency.py` 的 `check_referenced_paths()` 增加第 6 项检查（ghost-file linter）：扫描 `.claude/skills/` 与 `.codex/skills/` 所有 `*.md`，禁止出现已废弃的 `PROJECT_GUIDE` / `briefing.md` / `open_questions.md`；仅在含"不创建/未注册/deprecated"等否定语境的行上豁免（这些行代表"合法禁令"，是 Skill 契约本身）。
- 可复用模式：Skill 的 frontmatter description / SKILL.md 正文 / docs/ 子目录这三层必须语义一致；任何三者之间的冲突都是 P1 缺陷；人工保证不可持续，必须 linter 门禁。
- 建议升级为 Guard/XCheck/Skill 规则：已固化为 `check_memory_consistency.check_referenced_paths()` 第 6 项（ghost-file linter）；GHOST_PATTERNS 与 NEGATION_CONTEXT 可随后续发现扩充。

## L6 Lesson 需带 type+maturity 字段
- 类型：decision
- 成熟度：verified
- 场景：v5.2 起，对照"Harness 不是目的，知识才是护城河"一文给出的 MECE 五类知识 + 三级成熟度模型，将 lesson 从"只有 status/priority"扩展为"附加 type + maturity"两个结构化字段。
- 风险：若缺乏类型/成熟度区分，`vibe-evolve` 的晋升判定只能依靠 frequency/severity 两个粗粒度指标；衰减策略也无锚点，导致经验库逐渐失真。
- 修复策略：在 `LESSONS_RULES.md` 定义 type ∈ {model,decision,guideline,pitfall,process}、maturity ∈ {draft,verified,proven}；在 `LESSONS.md` 索引补 2 列；在 `evolution/lesson-index.json` 每条加 2 字段；在 `check_memory_consistency.py` 加 lint：active/Pinned 条目缺字段则报 ERROR，draft 在活跃窗口超过阈值则 WARN；在 `evolution-policy.md` 把 maturity 引入晋升判定。
- 可复用模式：知识条目的元数据 schema 是经验库可演化的前提；schema 变更必须同步：rules + 索引格式 + JSON schema + linter，缺一则漂移。
- 建议升级为 Guard/XCheck/Skill 规则：本条由 linter（check_memory_consistency 新增 lesson-schema 检查）守护；type+maturity → proven 的固化路径见 `evolution-policy.md`。

## L7 Lesson 引用追踪闭环（v5.3）
- 类型：process
- 成熟度：verified
- 场景：v5.2 让 lesson 有了 type+maturity 元数据，但活跃窗口是否还"活"——即是否在 EXEC/PLAN/CHANGELOG 等阶段产物中被真实引用——没有任何指标，长期未引用的 lesson 会逐渐变成知识库噪声。
- 风险：（1）经验库无限膨胀；（2）`vibe-evolve` 衰减判定无锚点；（3）代理读取 active 窗口仍然看到陈旧条目，稀释注意力。
- 修复策略：在 `evolution/lesson-index.json` 为每条 lesson 增加 `last_referenced` / `reference_count` / `referenced_in` 三字段；`scripts/check_memory_consistency.py` 新增扫描函数 `scan_lesson_refs()`，遍历 `memory-bank/progress.md`、`activeContext.md`、`architecture.md`、`docs/AI_CHANGELOG.md`、`evolution/promotion-log.md`、`plans/**/*.md`，按裸 `L\d+` 提取并就近继承 ISO 日期；`--strict` 仅读+WARN，`--update-refs` 写回（merge 而非覆盖，保留 type/maturity/promotion_status 等已有字段）。
- 可复用模式：知识条目应当被工作流"使用"才算活——给经验库装一个"心跳监测"，零引用即衰减信号；checker 默认只读避免与正常工作流的 diff 噪声混淆，写回单独命令。
- 建议升级为 Guard/XCheck/Skill 规则：保留为 process lesson；若日后扫描语料扩展到更多目录或检测多语义形式（lessonRefs YAML），可固化为独立 skill `vibe-lesson-refs`。

## L8 时间序日志标题前缀与孤儿页面守护（v5.4）
- 类型：decision
- 成熟度：verified
- 场景：v5.3 完成后，对照 Karpathy《LLM Wiki》gist 的 log.md 约定与"Lint 操作"，发现仓库内三个时间序文件（`docs/AI_CHANGELOG.md`、`evolution/promotion-log.md`、`memory-bank/progress.md`）使用不一致的 `## YYYY-MM-DD (...)` 标题格式，`grep` 难以稳定抽取最近时间线；`docs/agents/*.md` 与 `memory-bank/*.md` 缺少与 catalog（AGENTS.md / memory-registry.yaml）的反向守护，新增孤儿文件不会被任何 linter 发现。
- 风险：（1）时间线不可机读 → 代理 / 人工查阅历史成本高；（2）catalog 漏登记 → 新建文件不会进入 bootstrap，知识"沉海"；（3）跨项目模板使用者复用时格式漂移无门禁。
- 修复策略：在 `check_memory_consistency.py` 加两个 WARN 级 linter——`check_log_prefix()` 强制 `## [YYYY-MM-DD] <kind> | <summary>` 格式（kind ∈ `{changelog, promote, lint, progress, evolve, ingest, decision}`）；`check_orphan_docs()` 做两向绑定（docs/agents/*.md 必须被 AGENTS.md 引用，memory-bank/*.md 必须被 memory-registry.yaml 列出）。统一把已存在的 11 个历史日期标题改为新格式。
- 可复用模式：日志类文件的标题应当机器可解析；catalog 与 content 必须双向绑定，单向引用会导致孤儿漂移；新增 lint 引入时一律 WARN 级（不阻塞 `--strict`），降低外部模板分叉的迁移成本。
- 建议升级为 Guard/XCheck/Skill 规则：保留为 decision lesson；linter 已落地，固化路径见 `check_memory_consistency.check_log_prefix()` / `check_orphan_docs()`。

## L9 Copilot 集成与三向同步（v5.5）
- 类型：decision
- 成熟度：verified
- 场景：v5.4 落地后，主力 agent 从 Codex/Claude 扩到 Copilot。Copilot 不具备 shell hook 通道（无 SessionStart/UserPromptSubmit/Stop），不能复用 `scripts/hooks/*.py` 的自动门禁；三个 agent 的 skill 根也分裂为 `.codex/skills` / `.claude/skills` / `.github/skills`。
- 风险：（1）治理四件套 skill 在三端漂移，Copilot 看到与 Codex/Claude 不一致的规则；（2）Copilot 无 Stop hook，COMPLETE 前决不调用 `check_memory_consistency.py --strict` 则仓库事实崩溃不被发现；（3）Copilot 可写入 `/memories/repo/`，与 `memory-bank/` 各持一份仓库事实会造成知识分裂。
- 修复策略：（a）`scripts/sync_vibe_skills.py` 改造为三向同步（`MIRRORS = {codex, copilot}`），新增 `diff_one()` 与 `_write_mirror()` 以及 `docs/` 子目录的 backup-restore 逻辑，保留 `diff()` 并集聚合器作为向后兼容 API；`check_memory_consistency.py` 的 `check_referenced_paths()` 改为遍历 `VIBE_SKILLS_MIRRORS` 并调用 `diff_one`。（b）重写 `.github/copilot-instructions.md` 为指针型，指向 AGENTS.md 单源契约并补充 Copilot 特定约束（无 hook 自律、`/memories/repo/` 禁用、三向同步要求）。（c）新增 `.github/instructions/governance.instructions.md`，通过 `applyTo` 在 memory-bank / LESSONS / evolution / vibe-* / hooks 路径被动注入治理提醒。（d）AGENTS.md §9/§10/§11/§12 同步加入 Copilot 触发面、无 hook 说明、COMPLETE 加锁、memory 边界与三镜像策略。（e）`memory-bank/memory-registry.yaml` 添加 `skill_roots.copilot` 与 `agent_targets` 块。
- 可复用模式：同一治理契约面多 agent 时，**单源 + 镜像** 优于各自维护；对没有 shell hook 的 agent，用 `applyTo` / 仓库级 instructions 等被动注入机制 + agent 自律代替主动 hook，补充一条强制的 COMPLETE-gate 命令表述；**试点镜像逻辑才可仅限治理四件套**，避免镜像肨胀冲击各 agent 特有能力 skill；mirror 的 `docs/` 云许多端分歧需在同步脚本内错车 backup-restore，不能用 `shutil.copytree` 简单覆盖。
- 建议升级为 Guard/XCheck/Skill 规则：保留为 decision lesson；同步与检查逻辑已固化在 `scripts/sync_vibe_skills.py` 与 `scripts/check_memory_consistency.py`；若未来出现第四个主力 agent，仅需在 `MIRRORS` 与 `VIBE_SKILLS_MIRRORS` 各添一行即可报装。

## L10 项目模式与 phase 切档（v5.6）
- 类型：decision
- 成熟度：verified
- 场景：v5.5 把治理面拉齐到三个 agent，但所有项目仍被默认按"managed_harness"接入；面对纯人工历史项目（无 AGENTS、无 memory-bank）或已有旧 vibe-* skill 的项目，硬切 managed 会触发大量误报、阻塞业务推进，并诱使代理为绕过门禁去伪造记录。来自 v5.1 的项目分类模型补齐了这一缺口。
- 风险：（1）对历史项目硬启 managed → 一开局就被 Stop hook block，团队对 harness 产生抗拒；（2）一律 bootstrap 会用单文件 v5.1 AGENTS.md 覆盖掉本仓库 Map 拆分结构，导致回归；（3）hook 行为不可分档 → 没有"只读侦察 / 仅治理面 block"的中间态。
- 修复策略：（a）`memory-bank/memory-registry.yaml` 顶层引入 `project_mode ∈ {new_project, vibe_managed_legacy, unmanaged_legacy}` 与 `harness_phase ∈ {discovery_only, shadow_harness, soft_gate, managed_harness}`，并集中声明 `governance_paths` 与 `hook_policy`。（b）`scripts/check_memory_consistency.py` 新增 `parse_registry_phase()` 与 `--print-phase` / `--warn-only`，并按 phase 自动降级（discovery/shadow 全部转 warn）。（c）`scripts/hooks/{memory_stop_guard,codex_stop_memory_guard}.py` 先调 `--print-phase`，按 phase 决定 block 策略：warn-only / 治理面 only / 全量 block。（d）入口 skill 四件套 `vibe-bootstrap` / `vibe-retrofit` / `vibe-discovery` / `vibe-exec` 分别承接三类项目接入流；**显式不纳入三向镜像**，由各 agent 自行维护。（e）`scripts/install_vibe_harness.py` 加固：识别 Map-style AGENTS.md，retrofit 模式默认写 `AGENTS.v5.6.draft.md` 而非覆盖，必须 `--overwrite-agents` 才强制替换。（f）`scripts/discover_project.py` 引入只读侦察。
- 可复用模式：harness 接入策略必须按项目"治理熟度"分档而非一刀切；hook 的 block/warn 行为应当由 registry 声明的 phase 驱动，而不是硬编码；入口 skill 是一次性接入工具，与日常生命周期 skill 分层，**不必三向同步**；脚手架工具（install / discover）面对 Map 化的契约文件须做防覆盖保护，draft 文件优先于直接替换。
- 建议升级为 Guard/XCheck/Skill 规则：保留为 decision lesson；phase 驱动的 hook 行为已固化于 `memory_stop_guard.py` / `codex_stop_memory_guard.py`；如未来要在 PreToolUse 层做更细的"只允许只读工具 / 仅治理面写入"分档，可在此基础上加 `pre_tool_phase_guard.py`。

## L11 安装后必须实测 agent hook 与 Copilot applyTo
- 类型：pitfall
- 成熟度：verified
- 场景：`platform_design` discovery 安装后复盘发现：Codex hook 配置使用 `/usr/bin/env python3`，在 Windows/PowerShell 环境无法执行；文档与 registry 声明 `.github/instructions/governance.instructions.md`，但 discovery/retrofit 未安装该文件；项目原有 Copilot instruction 对 `**` 全量生效，可能与 harness 生命周期叠加冲突。
- 风险：（1）Codex/Claude 自动门禁看似已安装但实际不触发；（2）Copilot 缺少治理面 `applyTo` 被动注入，治理文件改动不会收到 MEMORY_CHECK / 三向同步提醒；（3）宽作用域 instruction 与 AGENTS.md 生命周期竞争，导致代理为满足所有模板而过度产出。
- 修复策略：安装器必须跳过缓存/本地产物，所有模式下补齐缺失的 Copilot governance instruction 与 Claude Stop hook 设置但不覆盖已有配置；Codex hook 命令必须跨 PowerShell / POSIX shell；`check_memory_consistency.py` 必须检查 governance instruction 文件存在与 `applyTo` 覆盖面；目标项目需要收窄既有 Copilot instruction 的 `applyTo`。
- 可复用模式：harness 安装完成不等于接入完成；至少实测一条 Session/Stop hook 命令、一次 Copilot governance applyTo 存在性检查、一次 `sync_vibe_skills --check` 和一次 memory check。
- 建议升级为 Guard/XCheck/Skill 规则：已固化到 `scripts/install_vibe_harness.py`、`.codex/hooks.json`、`.claude/settings.example.json`、`scripts/check_memory_consistency.py` 与 `docs/agents/hooks-and-commands.md`。

## L12 默认上下文必须预算化并按需展开
- 类型：decision
- 成熟度：verified
- 场景：v5.6 的默认 MEMORY_BOOTSTRAP 会读取 AGENTS、registry、progress、architecture、tech-stack、LESSONS、lesson-index 等约 50KB 内容；普通任务还会额外触发 skill 正文和工具输出，导致 token 成本长期偏高。
- 风险：（1）每轮会话为低风险任务支付 full governance 成本；（2）重要规则被大量历史上下文稀释；（3）业务项目接入 harness 后对 token 成本敏感，容易绕开治理。
- 修复策略：把 `read_policy` 改为 `light / standard / full` 三档；默认 `light` 只读契约、registry 与当前焦点；普通任务按需升到 `standard`；治理路径、高风险、失败复盘和 LESSONS/EVOLVE/memory 变更才升到 `full`；默认 `lean` skill 面只暴露核心 8 个，完整 Codex 技能库必须显式 `--skill-set full`；用 `scripts/context_budget.py` 和 checker 守住预算。
- 可复用模式：上下文和技能面都不是越多越安全；稳定契约进 AGENTS，真实事实进 profile，历史经验和高级 skill 只按风险/明确场景展开，并用预算工具量化。
- 建议升级为 Guard/XCheck/Skill 规则：已固化为 `read_policy.profiles`、`scripts/context_budget.py` 与 `check_memory_consistency` 的 profile/budget lint；无需新增 skill。
