# Vibecoding 稳定性版本（P7）

## 目标
对抗“复杂度熵增”与“最后 10% 陷阱”，让 AI 产出可维护、可审计、可回归。

## 核心机制
1. Flight Recorder（黑匣子）：每次非平凡代码变更必须记录到 `docs/AI_CHANGELOG.md`
2. Complexity Impact Score：变更复杂度评分（0-10）+ 风险分析
3. Deep-water Guard：检测进入深水区信号（高分频繁/热点文件/无文档）
4. Doc↔Code 一致性：审计读取 changelog 并校验“有 Doc 才有 Code”

## 文件
- `docs/AI_CHANGELOG.md`
- `scripts/log_change.py`
- `scripts/changelog_guard.py`
