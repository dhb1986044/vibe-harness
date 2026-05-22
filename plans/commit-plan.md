# Commit Plan

## [2026-05-22] git | initial publish to GitHub

## 目标
- 将当前 `vibe-harness-v5` 工作目录初始化为 Git 仓库。
- 创建一次原子提交，发布当前 v5.6 harness 模板状态。
- 推送到 `https://github.com/dhb1986044/vibe-harness.git`。

## 现状
- `D:/workspace/vibe-harness-v5` 当前不是 Git 工作树，缺少 `.git/`。
- 远端 `https://github.com/dhb1986044/vibe-harness.git` 的 `ls-remote --heads` 未返回可见分支，按空仓库首次推送处理。
- 仓库包含治理契约、memory-bank、docs、scripts、agent skills 与 v5.1 source snapshot。

## 提交拆分

### Commit 1: `chore: publish vibe harness v5.6`
- 范围：当前项目文件、治理记录、首次提交计划、根 `.gitignore` 与 `.gitattributes`。
- 排除：Python 缓存、`.serena/` 本地工具状态、环境文件与本地配置。
- 换行：通过 `.gitattributes` 统一文本文件 LF，降低跨平台换行漂移。
- 命令：
  - `git init -b main`
  - `git remote add origin https://github.com/dhb1986044/vibe-harness.git`
  - `git add .`
  - `git commit -m "chore: publish vibe harness v5.6"`
  - `git push -u origin main`

## 检查项
- `python scripts/check_memory_consistency.py --strict`
- `git status --short`
- `git ls-remote --heads https://github.com/dhb1986044/vibe-harness.git`
- 敏感词扫描：`api_key|secret|token|password|cookie|BEGIN PRIVATE KEY`

## 回滚策略
- 提交前：删除本地 `.git/` 即可回到非 Git 目录状态。
- 提交后、推送前：`git reset --soft HEAD~1` 可撤回提交但保留文件。
- 推送后：优先创建修正提交；如必须回退远端历史，需要用户再次确认后才允许强制操作。

## 风险评估
- 风险等级：中。
- 主要风险：首次推送会公开当前目录内容到指定远端；远端若存在未发现历史，push 可能被拒绝。
- 缓解：提交前排除缓存和本地状态，执行 memory consistency 与敏感词扫描。
