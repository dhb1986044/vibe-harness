# 纯人工历史项目接入手册：vibe-discovery

目标：先考古，再建档，再接管。

## 阶段 0：只读冻结

禁止改代码、删文件、重构、启用 blocking hook。

## 阶段 1：Discovery

运行：

```bash
python scripts/discover_project.py --write
```

生成：

- `PROJECT_DISCOVERY_REPORT.md`
- `memory-bank/*.draft.md`

## 阶段 2：人工确认

确认启动、测试、构建、部署、敏感配置、危险目录。

## 阶段 3：Shadow Harness

启用 AGENTS 和 memory，但 hooks 只 warning。

## 阶段 4：Soft Gate

仅治理文件阻断。

## 阶段 5：Managed Harness

完整启用 XCHECK / GUARD / EVOLVE / MEMORY_CHECK。
