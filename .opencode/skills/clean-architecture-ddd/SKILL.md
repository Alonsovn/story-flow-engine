---
name: clean-architecture-ddd
description: Enforce domain/application/infrastructure boundaries and suggest correct placements
compatibility: opencode
metadata:
  architecture: clean
  style: ddd
---

## What I do

- Review proposed changes for boundary violations (dependencies must point inward).
- Recommend where code should live (domain vs application vs infrastructure vs presentation).
- Suggest interfaces (ports) and adapters (implementations) when integrating external systems.

## When to use me

- When adding new features or integrating external services (e.g., Jira, databases).
- When refactoring or reorganizing packages.

## Heuristics

- Domain: pure business rules, no IO, no framework imports.
- Application: orchestrates use cases, depends on domain and interfaces.
- Infrastructure: IO and external integrations, implements application interfaces.
- Presentation: FastAPI routes/schemas/dependencies.
