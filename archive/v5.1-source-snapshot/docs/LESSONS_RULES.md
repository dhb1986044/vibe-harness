# LESSONS Rules v5.1

## 文件职责

- `docs/LESSONS.md`：主经验库，只保留索引、Pinned 和活跃窗口。
- `docs/LESSONS_ARCHIVE.md`：归档库，默认不读全文。
- `evolution/lesson-index.json`：可计算索引。
- `evolution/promotion-log.md`：晋升记录。

## 默认读取协议

1. 先读 Active Summary 和索引。
2. 默认展开 Pinned + 最近 5~10 条活跃 lesson。
3. 命中标签、关键词、模块或同类失败时，再展开旧条目或 archive。
4. 禁止默认通读全文。

## 索引字段

| # | 标题 | 标签 | 优先级 | 状态 |
|---|---|---|---|---|

状态：`活跃` / `已归档` / `Pinned`。

## 活跃窗口

- 活跃条目软上限：12
- 推荐窗口：8~10
- Pinned 不计入默认归档优先级

## 晋升规则

重复、高风险、可复用、可自动化的 lesson 必须判断是否晋升为：

```text
Guard / XCheck / Skill / Template / Plugin
```

## 去重规则

同一反模式优先更新已有 lesson，不新开编号。
