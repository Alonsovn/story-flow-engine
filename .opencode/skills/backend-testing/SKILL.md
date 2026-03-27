---
name: backend-testing
description: Run pytest, interpret failures, and suggest fixes without breaking architecture
compatibility: opencode
metadata:
  stack: python
  framework: pytest
  scope: backend
---

## What I do

- Run the test suite with `python3 -m pytest` (optionally targeted to a file/test).
- If tests fail, identify the failing assertion(s) and likely root cause.
- Propose a minimal fix consistent with Clean Architecture boundaries.

## When to use me

- After changing any domain/application/infrastructure code.
- When CI fails or a regression is suspected.

## Guardrails

- Never “fix” tests by skipping, deleting, or loosening assertions.
- Prefer small, incremental fixes.
- If a fix requires changing public behavior, call it out and ask for confirmation.
