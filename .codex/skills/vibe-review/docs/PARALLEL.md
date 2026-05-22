# 并行任务（Parallel Tasks）—Windows 实操

## 目标
用 **Git worktree + 多终端会话** 实现“像有 3-10 个助手一样”并行推进：
- 前端/后端/数据/文档/审计/测试 分工并行
- 每个会话绑定一个 worktree + 分支，互不干扰

## Windows 推荐布局（PowerShell）
### 1) 创建 3 个 worktree（示例）
```powershell
git fetch --all
git worktree add ..\wt-a -b feat/a
git worktree add ..\wt-b -b feat/b
git worktree add ..\wt-c -b feat/c
```

### 2) 打开多个终端（每个 worktree 一个）
```powershell
wt -d ..\wt-a
wt -d ..\wt-b
wt -d ..\wt-c
```

### 3) 每个终端启动一个 AI 会话
- 终端 A：实现功能
- 终端 B：写测试/跑 lint
- 终端 C：写文档/更新 memory-bank
- 预留一个“分析终端”：只看日志/跑脚本（不写代码）

## 命名/切换建议
- 统一分支命名：`feat/a`, `fix/b`, `chore/docs`
- 终端 Tab 改名：A/B/C/ANALYZE
- 每个会话开头强制写入：`memory-bank/activeContext.md` 当前分工与边界
