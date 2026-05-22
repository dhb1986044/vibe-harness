# 数据分析集成（AI Data Analyst）

## 目标
让 AI 能在开发中即时查询/验证数据（SQL/日志/指标）。

## 接入方式（不依赖 MCP）
- 通过 CLI 工具（如 psql/mysql/sqlite/duckdb/bq 等）
- 通过内部 HTTP API（若有）

## 安全建议
- 最小权限
- 脱敏
- 查询结果落盘到 `memory-bank/progress.md`（只保留必要摘要）
