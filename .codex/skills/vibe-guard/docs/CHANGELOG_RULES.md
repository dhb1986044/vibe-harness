# ChangeLog 规则（强制）

## Code follows Doc
每条日志必须标注依据的文档：`--doc <path>@<version>`

## No Doc, No Code
无 doc ref 会被标记为风险信号，需补齐文档或回滚代码。

## 最小必填
- change_type（Feature/Bugfix/Refactor/Critical-Fix）
- summary（技术摘要）
- risk_analysis（诚实风险评估）
- files_touched（至少列出关键文件）
- regression checklist（至少 1 条可验证检查项）
