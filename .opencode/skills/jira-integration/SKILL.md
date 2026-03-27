---
name: jira-integration
description: Implement Jira repository adapters using httpx/respx with safe auth/config patterns
compatibility: opencode
metadata:
  integration: jira
  libs: httpx,respx
---

## What I do

- Implement or extend Jira repository adapters (infrastructure) behind `JiraRepository` (application port).
- Use `httpx` async client patterns and `respx` for tests.
- Keep credentials in environment/config (never hardcode).

## When to use me

- When adding new Jira endpoints (epics, stories, transitions, search).
- When tests need stable HTTP mocking.

## Guardrails

- Do not import infrastructure into domain.
- Keep Jira field IDs configurable (e.g., story points custom field).
