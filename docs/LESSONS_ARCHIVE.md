# Lessons Archive

归档库。默认不进入 Memory Bootstrap，只有命中标签、关键词、模块或同类失败时才读取。

## [2026-05-22] archive | L4 harness 模板不应打包业务专属 skill
- 归档原因：新增 L11 后，为保持 Active 窗口在 10 条，将较早且本轮未直接命中的 L4 移入 archive；索引保留为 `已归档`，命中 Skills/Architecture 或 harness 纯净性问题时再展开。

## L4 harness 模板不应打包业务专属 skill
- 类型：guideline
- 成熟度：verified
- 场景：vibe-harness-v5 从 badcase-miner 项目移植过来的 vibe-* skill 中，`vibe-knowledge-modifier` 详细说明引用了 `evolution_analysis_*.md`、特定规则集等 badcase-miner 业务附件；`vibe-review` 硬编码了 L2-L9 与该项目业务耦合的教训编号；`vibe-data`/`vibe-prompt`/`vibe-parallel` 也不属于通用治理闭环。
- 风险：（1）使用者安装 harness 后获得不可用的 skill，调用时读不到附件报错；（2）硬编码的教训编号会在新项目被误读；（3）增加 harness 表面积但不提供价值。
- 修复策略：纳入 skill 前按三问检查：（a）能否在不依赖任何业务附件的情况下运行？（b）内部是否硬编码了某项目的教训编号/名字/列号？（c）是否是"仅治理闭环"中任一环节的一部分（INIT/PLAN/EXEC/XCHECK/GUARD/CHANGELOG/LESSONS/EVOLVE/MEMORY_CHECK）？任何一项为否则不进入 harness。
- 可复用模式：harness 纯净原则 — 只装 universal governance，不装 example workflow；业务 skill 留在业务 repo。
- 建议升级为 Guard/XCheck/Skill 规则：待观察；若同类问题出现第 2 次，则在 `vibe-evolve` 中增加"new skill admission checklist"门禁。
