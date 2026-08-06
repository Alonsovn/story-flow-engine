# Story Flow Engine

A powerful CLI tool that transforms structured Markdown files into Jira issues. Built with Clean Architecture and Domain-Driven Design principles.

## Overview

Story Flow Engine automates the conversion from structured Markdown to Jira issues. Product teams write detailed epics and user stories in Markdown files during planning sessions, but manually creating these artifacts in Jira is time-consuming and error-prone. This tool bridges that gap.

## Features

- **Markdown Parsing**: Parse structured epic and user story templates from Markdown files
- **Jira Integration**: Create issues directly in Jira via REST API
- **Hierarchical Support**: Manage Epic → Stories relationships
- **Dry-Run Mode**: Validate everything before actual Jira creation
- **Extensible Architecture**: Built for future API support (FastAPI)
- **Beautiful CLI Output**: Rich formatting for parsed data display

## Tech Stack

| Component | Technology |
|-----------|------------|
| CLI | Typer + Rich |
| API Client | `jira` library + httpx |
| Validation | Pydantic v2 |
| Parsing | `markdown-it-py` |
| Config | python-dotenv + pyaml-env |
| Testing | pytest + pytest-mock |

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd story-flow-engine

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Jira credentials
```

## Configuration

### Environment Variables

Create a `.env` file with your Jira credentials:

```bash
APP_ENV=local
LOG_LEVEL=debug

# Jira Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token
JIRA_PROJECT_KEY=PROJ
JIRA_DEFAULT_ISSUE_TYPE=Story
JIRA_DEFAULT_PRIORITY=Medium
```

## Usage

### Parse Markdown Files

```bash
# Parse a sample epic

python -m src.main parse data/EPIC-0-foundational/epic.md

# Parse sample stories
python -m src.main parse data/EPIC-0-foundational/stories.md

# Parse and display extracted entities
python -m src.main parse <path-to-markdown>

# Output in JSON format
python -m src.main parse <path> --format json

# Parse only epics
python -m src.main parse <path> --epics-only
```

### Create Jira Issues

```bash
# Dry run with sample data (validate without creating)
python -m src.main create data/EPIC-0-foundational/ --project PROJ --dry-run

# Create issues in Jira
python -m src.main create <path> --project PROJ
```

### Configuration Management

```bash
# Display current configuration
python -m src.main config show

# Validate configuration
python -m src.main config validate
```

## Markdown Format

Place your own epics and user stories inside the `data/` directory, following the EPIC-0 convention: one subfolder per epic (e.g., `data/EPIC-1-my-feature/`) containing an `epic.md` and a `stories.md` file. The `data/.gitkeep` file ensures the directory is tracked in version control.

### Epic Format

```markdown
# Epic: Project and Local Development Setup (Foundational)

**Epic Title**: Project and Local Development Setup (Foundational)
**Epic Key**: EPIC-0
**Summary**: Establish foundational project structure...
**Labels**: foundational, setup, ci-cd
**Priority**: Must Have
**Components**: Backend, Frontend, Database
**Fix Version**: MVP-1

---

**Epic Description:**
Problem Statement: Delivery teams cannot begin engineering work...

Objective: Establish the foundational project structure...

Included scope:
- Repository structure and folder organization
- Local development environment setup (Python, Node.js, Docker, database)
- CI/CD pipeline scaffolding and basic testing framework integration

Excluded scope:
- Feature-specific implementation beyond structure and scaffolding
- Advanced deployment automation or multi-region strategies

Dependencies:
- [Architecture Solution Design](../../03-architecture/architecture-solution-design.md)
- [Technology Stack](../../03-architecture/technology-stack.md)

Measurable success criteria:
- Every engineer can clone and run local dev environments in under 15 minutes.
- CI/CD pipeline runs on every commit and reports clear pass/fail status.
```

### User Story Format

```markdown
### US-EP0-BE-001: Backend Modular Monolith Structure and Scaffolding

**Story ID**: US-EP0-BE-001
**Epic Link**: EPIC-0
**Priority**: Must Have
**Effort Estimate**: 8

**As a** Backend Engineer,
**I want to** establish a backend modular monolith repository structure,
**So that** all team members can develop and test code with consistent project organization.

**Acceptance Criteria**:
- [ ] Given the backend repository is cloned, then folder structure includes modules/, shared/, config/, and tests/ directories.
- [ ] Given a developer runs setup script, then all dependencies are installed and project is ready for local development.

**Deliverables**:
- Backend repository root with modules/, shared/, config/, and tests/ directories.
- Setup script for fast local environment configuration.

**Dependencies**:
- [Architecture Solution Design](../../03-architecture/architecture-solution-design.md).
- [Technology Stack](../../03-architecture/technology-stack.md).

**Success Metrics**:
- First-time setup completes in under 15 minutes.
- All imports follow agreed pattern.
```

## Architecture

The project follows **Clean Architecture** principles with **Domain-Driven Design**:

```
src/app/
├── main.py                     # Entry point
├── config/                     # YAML-based configuration management
├── domain/
│   ├── entities/               # Epic, UserStory
│   ├── value_objects/          # IssueId, Label, Priority, StoryPoints
│   └── exceptions/             # Business rule, not found, duplicate, etc.
├── application/
│   ├── use_cases/              # GetEpicWithStories
│   ├── dtos/                   # EpicDTO, StoryDTOs
│   ├── interfaces/             # JiraRepository port
│   └── mappers/                # Entity ↔ DTO mapping
├── infrastructure/
│   ├── external/jira/          # Jira API client (httpx-based)
│   └── logging/                # Structured logging
├── presentation/
│   └── cli.py                  # Typer CLI commands
└── shared/
    ├── global_variables.py
    └── utils/                  # Retry decorator, log utilities
```

### Domain Layer

- **Entities**: `Epic`, `UserStory` — core business objects with behavior
- **Value Objects**: `IssueId`, `Priority`, `StoryPoints`, `Label` — immutable, self-validating
- **Exceptions**: `BusinessRuleViolation`, `NotFoundError`, `DuplicateStoryError`, `InvalidTransitionError`, `UnauthorizedAccessError`

### Application Layer

- **Use Cases**: `GetEpicWithStories` — orchestrates domain logic
- **DTOs**: `EpicDTO`, `StoryDTO` — data transfer objects for boundaries
- **Interfaces**: `JiraRepository` — port defining Jira operations
- **Mappers**: `EpicMapper` — transforms between domain entities and DTOs

### Infrastructure Layer

- **Jira Client**: `JiraApiRepositoryImpl` — httpx-based REST client implementing `JiraRepository`
- **Logging**: Structured logger with retry decorator for transient failures

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/domain/
```

### Code Style

The project follows these conventions:

- **Python Style Guide**: PEP 8
- **Naming**: camelCase for variables, PascalCase for classes
- **Type Hints**: Full type hints on all functions
- **Docstrings**: Google-style docstrings


## License

MIT License - see [LICENSE](LICENSE) for details.
