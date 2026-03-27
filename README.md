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
# Parse and display extracted entities
python -m src.main parse <path-to-markdown>

# Output in JSON format
python -m src.main parse <path> --format json

# Parse only epics
python -m src.main parse <path> --epics-only
```

### Create Jira Issues

```bash
# Dry run (validate without creating)
python -m src.main create <path> --project PROJ --dry-run

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

### Epic Format

```markdown
## Epic 1: Client and Project Lifecycle Governance

**Problem Statement:** Freelancers need...

**Objective:** Provide a stable...

Included scope:
- Item 1
- Item 2

Excluded scope:
- Item 1

Dependencies:
- [Link](./other-doc.md)

Acceptance criteria:
- Given..., when..., then...
```

### User Story Format

```markdown
### US-MVP-BE-001: Admin Authentication Service

**Epic**: Epic 1
**Priority**: Must Have
**Effort Estimate**: 8

**As a** Backend Engineer,
**I want to** implement secure auth,
**So that** Admin users can log in safely.

**Acceptance Criteria**:
- [ ] Given..., when..., then...
- [ ] Given..., when..., then...
```

## Architecture

The project follows **Clean Architecture** principles with **Domain-Driven Design**:

```
src/app/
├── main.py                 # Entry point
├── config/                 # Configuration management
├── features/
│   ├── cli/               # CLI commands
│   └── jira/              # Jira integration
│       ├── domain/        # Entities, value objects, services
│       ├── application/   # Use cases, DTOs
│       └── infrastructure/# External implementations
```

### Domain Layer

- **Entities**: Epic, UserStory, JiraProject
- **Value Objects**: StoryId, Priority, EpicId
- **Domain Events**: EpicCreated, StoryCreated

### Application Layer

- **Use Cases**: ParseMarkdown, CreateJiraIssues, DryRun
- **Services**: MarkdownParser, JiraMapper, StoryFlowService
- **Ports**: MarkdownReader, JiraClient interfaces

### Infrastructure Layer

- **Parsers**: EpicParser, StoryParser
- **Jira Client**: JiraHttpClient, ResponseMapper

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
