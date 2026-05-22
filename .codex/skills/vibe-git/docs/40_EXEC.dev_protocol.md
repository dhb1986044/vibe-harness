# EXEC Protocol (Execution)

- Implement only the next approved plan step.
- Prefer TDD; add/adjust tests for behavior changes.
- Explicit logging and fail-visible behavior; no silent failures.
- No secrets in code; use `.env` / config files.
- Keep modules small; avoid monolithic files.
- After execution: update memory-bank (activeContext/progress; architecture if needed).
