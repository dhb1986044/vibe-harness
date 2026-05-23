# 进度日志

> 请根据项目实际情况维护本文件。vibe-harness 只提供模板，不替代真实项目事实。

## 初始化骨架（按时间倒序，最新的在最上面）

## [2026-05-23] progress | v5.7 默认上下文 profile 与预算门禁
- 已完成：将 harness 默认读取策略从固定 full bootstrap 改为 `read_policy.profiles` 三档；`light` 默认读取 AGENTS、registry、activeContext，预算 12KB；`standard` 读取架构/命令/最近进展与少量 LESSONS，预算 24KB；`full` 保留 v5.6 `bootstrap_order`。新增 `scripts/context_budget.py`，`check_memory_consistency.py` 接入 profile schema/budget lint；`install_vibe_harness.py` 新增 `--context-profile` 与 `--skill-set {lean,full}`，默认轻量安装且不删除目标已有 skill；Codex SessionStart 改为提示 profile 和 LESSONS 触发条件。同步更新 AGENTS、docs/agents、README_DEPLOYMENT、Copilot governance applyTo，并新增 L12。已执行 py_compile、light/standard/full budget、strict memory check、sync check、SessionStart smoke、三组安装器 dry-run、旧 registry warn-only 回归。关联 lessons：L1 L2 L3 L7 L8 L10 L11 L12。
- 进行中：无。
- 阻塞 / 风险：无当前阻塞。GUARD 风险等级：中；回滚方式为 `git restore` 本轮触达文件并删除新增 `scripts/context_budget.py`；残余风险是现有已安装项目需要重新运行 retrofit 或手动合并 AGENTS/registry 才能获得 light 默认。
- 下一步：如需应用到 `platform_design`，先用 `install_vibe_harness.py --target D:/workspace/wl/platform_design --mode retrofit --context-profile light --skill-set lean --dry-run` 复核，不直接覆盖业务文件。

## [2026-05-22] progress | platform_design 安装复盘后的 harness 加固
- 已完成：根据 `D:/workspace/wl/platform_design` discovery 安装复盘，修复源仓 `.codex/hooks.json` 的 POSIX 专属 `/usr/bin/env` 命令，改为 PowerShell/POSIX 均可展开的 `python "$(git rev-parse --show-toplevel)/..."`；`.claude/settings.example.json` 改用 `python`；`scripts/install_vibe_harness.py` 增加缓存/本地产物跳过、缺失 Copilot governance instruction 补齐、缺失 Claude Stop hook 设置补齐且不覆盖已有配置；`scripts/check_memory_consistency.py` 增加 `.github/instructions/governance.instructions.md` 存在性与 `applyTo` 覆盖检查；`scripts/evolve_lessons.py` 修正 tags 写回，避免 JSON tags 从数组退化为字符串；`docs/agents/` 同步说明跨平台 hook 与安装器职责。目标项目同步应用同等修正，并补 `.claude/settings.json`、`.github/instructions/governance.instructions.md`，收窄原 `spec-driven-workflow-v1.instructions.md` 的 `applyTo`。新增 L11，归档 L4，运行 `python scripts/evolve_lessons.py --write`。关联 lessons：L1 L2 L7 L8 L9 L10 L11。
- 进行中：无。
- 阻塞 / 风险：未删除源仓与目标项目中已存在的 `scripts/**/__pycache__` 缓存目录，因为删除文件/目录需明确确认；这些目录已被 `.gitignore` 忽略，安装器后续不会再复制。残余风险是不同 agent 对 hook command 的执行 shell 可能存在差异，已用当前 PowerShell 路径做 smoke。
- 下一步：等待用户确认是否删除已忽略的 `scripts/**/__pycache__` 缓存目录；若不删除，不影响版本控制或后续安装。

## [2026-05-22] progress | 首次 Git 发布到 GitHub
- 已完成：确认当前目录不是 Git 工作树，远端 `https://github.com/dhb1986044/vibe-harness.git` 未返回可见分支；按首次发布处理。新增根 `.gitignore` 排除 Python 缓存、`.serena/` 本地工具状态、环境文件和 OS/editor 噪声；新增 `.gitattributes` 统一文本文件 LF；生成 `plans/commit-plan.md` 记录提交范围、检查项和回滚策略。已执行 lesson 引用回填、`python scripts/check_memory_consistency.py --strict`、基础敏感词扫描、Python 语法检查、`git diff --cached --check`，并创建首次内容提交 `5a8bc5c chore: publish vibe harness v5.6`。`git push -u origin main` 已成功创建远端 `main` 分支，`git ls-remote --heads origin main` 返回 `5a8bc5c1386367fa266b8ced6d51baa73943d564`。关联 lessons：L1 L2 L7 L8 L10。
- 进行中：无。
- 阻塞 / 风险：无当前阻塞。残余风险是 GitHub 仓库默认分支保护或页面索引延迟不会影响已完成的 `main` 分支推送；不进行强制覆盖。
- 下一步：无。

## [2026-05-19] progress | evolve schema merge + PreTool guard 加固
- 已完成：按研究报告与计划做小步治理脚本稳固——`scripts/evolve_lessons.py` 支持 7 列 LESSONS 索引并把 `--write` 改为 schema-safe merge，保留 v5.6 `lesson-index.json` 里的 `type` / `maturity` / 引用追踪 / 历史 promotion 字段；`scripts/hooks/codex_pre_tool_guard.py` 扩展跨平台危险命令拦截，覆盖 git 强制破坏、Linux 根目录递归删除、PowerShell 递归强制删除、Windows 递归静默删除。同步 `docs/AI_CHANGELOG.md` 与 `activeContext.md`，并用 `--update-refs` 回填 lesson 引用。关联 lessons：L1 L2 L6 L7 L8 L10。
- 进行中：无。
- 阻塞 / 风险：无阻塞。残余风险是 PreTool 正则只覆盖明确高风险组合，不尝试理解所有 shell 语义；`evolve_lessons.py --write` 的真实候选文件生成仍需在后续晋升任务中人工 review。
- 下一步：后续如再次运行 `python scripts/evolve_lessons.py --write`，观察候选输出是否符合预期；如新增危险命令模式，优先扩展现有正则表，不引入复杂策略引擎。

## [2026-05-12] progress | v5.5 Copilot 集成 + 三向同步
- 已完成：把 Copilot 接入 vibe-harness 治理体系——`scripts/sync_vibe_skills.py` 改为三向同步（`.claude/skills` → `.codex/skills` + `.github/skills`，`docs/` 子目录三端允许分歧）；`check_memory_consistency.py` 把 `VIBE_SKILLS_MIRRORS` 扩为多镜像遍历；`.github/copilot-instructions.md` 重写为 AGENTS.md 指针 + Copilot 特定约束；新增 `.github/instructions/governance.instructions.md`（applyTo 被动注入）；`AGENTS.md` §9/§10/§11/§12 加入 Copilot 三层兜底（仓库级 instructions + applyTo + agent 自律）与 `.github/skills/vibe-*/**` 触发面；`docs/agents/hooks-and-commands.md` 加 Copilot 章节；`memory-bank/memory-registry.yaml` 升 v5.5（`skill_roots.copilot` + `agent_targets.copilot.memory_policy.repo_scope_forbidden: true`）；新增 L9（decision/verified）。`sync --check` 与 `--strict` 均 PASS。关联 lessons：L1 L2 L3 L9。
- 进行中：无。
- 阻塞 / 风险：`scripts/evolve_lessons.py --write` 仍是 v5 schema 硬编码，会覆盖 v5.2/v5.3/v5.4/v5.5 增量字段；下次涉及 evolve 写回前必须先修。

## [2026-05-12] progress | v5.4 日志前缀 + 孤儿守护 linter
- 已完成：参考 Karpathy《LLM Wiki》gist 的 log.md 约定 + Lint 操作，落地 v5.4 ——`scripts/check_memory_consistency.py` 加 `check_log_prefix()` + `check_orphan_docs()` 两个 WARN 级 linter；统一 11 条历史日期标题为 `## [YYYY-MM-DD] <kind> | <summary>`；新增 L8（decision/verified）；`lesson-index.json` 与 `memory-registry.yaml` 升级到 v5.4。`--strict` PASS 无 log-prefix / orphan WARN。关联 lessons：L1 L3 L6 L7 L8。
- 进行中：无。
- 阻塞 / 风险：`scripts/evolve_lessons.py --write` 仍是 v5 schema 硬编码，会覆盖 v5.2/v5.3/v5.4 增量字段；下次涉及 evolve 写回前必须先修。
- 下一步：观察 v5.4 在新任务中的命中情况；如需要可把 log-prefix 升级为 ERROR 级强制；或扩展 orphan-docs 到 `.codex/skills/**`、`.claude/skills/**` 的 catalog 守护。

## [2026-05-12] progress | lesson 引用追踪闭环 v5.3 + docs/agents Layer B 摘要
- 已完成：lesson 引用追踪闭环 v5.3 落地——`evolution/lesson-index.json` 每条 lesson 加 `last_referenced` / `reference_count` / `referenced_in` 三字段；`scripts/check_memory_consistency.py` 加 `scan_lesson_refs()` + `--update-refs` 写回（merge，不覆盖 v5.2 schema）；活跃 / Pinned 零引用 WARN；字段漂移 WARN；schema_version → v5.3；registry → v5.3。`docs/agents/{lifecycle,memory-model,lessons-policy,evolution-policy,safety-and-completion,hooks-and-commands}.md` 顶部加 Layer B 摘要（何时该读 / 包含内容 / 不在此处）。新增 L7。`--strict` PASS。关联 lessons：L1 L2 L3 L6 L7。
- 进行中：无。
- 阻塞 / 风险：bundled `vibe-memory-check/scripts/check_memory_consistency.py` 仍是旧版（与 v5.2 / v5.3 root 版本漂移）；运行时使用的是 root 脚本，对 hook 路径无影响；后续若需消除可同步更新。
- 下一步：观察 v5.3 引用追踪在新任务中的命中情况；若发现某些 plans/ 目录或非常规产物未被扫描，再扩展 `LESSON_REF_SCAN_GLOBS`；当 active 窗口出现长期零引用条目时（≥6 月 verified / ≥12 月 proven），由 `vibe-evolve` 提名归档。

## [2026-05-12] progress | lesson schema v5.2 落地
- 已完成：lesson schema v5.2 落地——`type` (5 类 MECE) + `maturity` (3 级) 字段写入 LESSONS_RULES.md / LESSONS.md / lesson-index.json；`check_memory_consistency.py` 加 lesson-schema lint；evolution-policy.md 引入 maturity 作为晋升锚点；memory-registry.yaml 声明 schema；新增 L6；`--strict` PASS。关联 lessons：L6。
- 进行中：无。
- 阻塞 / 风险：bundled skill 内 `vibe-memory-check/scripts/check_memory_consistency.py` 仍是旧版（不解析新列），但 AGENTS.md 与 registry 引用的是根 `scripts/`，对运行时无影响；如需消除漂移，后续可同步更新。
- 下一步：观察新 schema 在实际任务中的使用；若进入"引用追踪闭环"演进，再扩展 progress.md / plans/ 产物中的 `lessonRefs` 字段。

## YYYY-MM-DD
- 已完成：
- 进行中：
- 阻塞 / 风险：
- 下一步：

## 里程碑
- [ ] M1：
- [ ] M2：
