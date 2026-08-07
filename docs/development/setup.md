# Development Setup

## Prerequisites

Same as [installation](../getting-started/installation.md), plus:
- A code editor (VS Code recommended)
- Familiarity with Python type hints and async/await

## Project Conventions

### Code Style

- **PEP 8** — standard Python style
- **camelCase** for variables and functions
- **PascalCase** for classes
- **Full type hints** on all function signatures
- **Google-style docstrings** with Args, Returns, and Raises sections

### Naming

| What | Convention | Examples |
|------|-----------|----------|
| Classes | PascalCase | `Epic`, `UserStory`, `JiraApiRepositoryImpl` |
| Functions/methods | camelCase | `get_epic`, `find_epics_by_project` |
| Variables | camelCase | `epicId`, `storyKey`, `jiraConfig` |
| Files | snake_case | `epic.py`, `user_story.py`, `jira_repository.py` |
| Test files | test_ prefixed | `test_epic.py`, `test_priority.py` |

### Type Hints

Every function signature must include type hints:

```python
async def get_epic(self, issue_id: IssueId) -> Optional[Epic]:
    ...
```

Use `Optional[X]` instead of `X | None` for consistency with the existing codebase.

### Docstrings

Google-style, always including parameter and return descriptions:

```python
def create(cls, key: str, summary: str) -> "Epic":
    """
    Factory method to create an Epic instance.

    Args:
        key: Jira issue key (e.g., "PROJ-123")
        summary: Epic title/summary

    Returns:
        New Epic instance

    Raises:
        BusinessRuleViolationException: If required fields are missing
    """
```

## Running the App

```bash
# Interactive mode
./scripts/run-cli

# Direct module
python -m src.app.presentation.cli
```

## Environment Switching

Set `APP_ENV` in `.env` to switch between YAML configs:

```bash
APP_ENV=local    # uses config_local.yml
APP_ENV=test     # uses config_test.yml
```

For running tests, the test config is loaded automatically by test fixtures.

## Directory Structure for New Features

When adding features, follow the existing layer structure:

```
src/app/
├── domain/
│   ├── entities/       # New entities with factory methods
│   ├── value_objects/  # New value objects (frozen dataclasses)
│   └── exceptions/     # New domain exceptions
├── application/
│   ├── use_cases/      # New use case classes
│   ├── dtos/           # New DTOs
│   ├── interfaces/     # New repository ports (ABCs)
│   └── mappers/        # New entity-to-DTO mappers
├── infrastructure/
│   └── external/       # New repository implementations
└── presentation/       # New CLI commands
```
