# Vibecoding 配置（P3）

本配置用于让“澄清必停 / EXEC 才能写入或执行 / 落盘路径统一”等行为可配置，避免每次手工改提示词。

## 环境变量（推荐）

### 1) 澄清问题数量门槛
- `VIBE_CLARIFY_MIN`：默认 `9`
  - Windows（PowerShell，当前会话）：
    ```powershell
    $env:VIBE_CLARIFY_MIN = "12"
    ```

### 2) 是否允许直接落盘（自动写 memory-bank/ 与 plans/）
- `VIBE_AUTOPERSIST`：默认 `1`
  - `1`：允许自动落盘（当工具允许写文件时）
  - `0`：只输出 path 块，不实际写文件

### 3) 是否允许执行阶段（写代码/跑命令/提交 git）
- `VIBE_EXEC_MODE`：默认 `0`
  - `0`：禁止执行与写文件（只读/只规划）
  - `1`：允许执行（等价于用户明确说“进入执行阶段（EXEC）”）

> 建议：对话里用一句“进入执行阶段（EXEC）”显式授权；该授权优先级高于环境变量。

## 默认落盘目录（工程内）
- `memory-bank/`
- `plans/`

## 强约束（不建议配置化）
- 规划阶段：必须 plan-only，不要直接写代码。
- 执行阶段：每个关键变更必须追加 `memory-bank/progress.md`。
