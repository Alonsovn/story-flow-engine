# AGENTS.md

This guide exists to help agentic tools, like Copilot, operate effectively within this repository. Follow these practices to maintain code quality and consistency while interacting with the project.

---

## 🚨 Non-Negotiable Rules

These rules are mandatory and must be followed at all times.

1.  **Never Commit Directly to `main`**: All changes must be submitted via a pull request.
2.  **Never Force Push**: Do not use `git push --force` on shared branches, especially `main`.
3.  **All Tests Must Pass**: Never commit code that breaks existing tests.
4.  **Do Not Remove or Disable Tests**: It is forbidden to comment out, skip, or delete tests to make a build pass. Always fix the underlying issue.
5.  **Adhere to TDD**: Follow the "Red-Green-Refactor" cycle for all new features and bug fixes.
6.  **Preserve Architecture**: Do not violate the Clean Architecture boundaries (`domain`, `application`, `infrastructure`).
7.  **No Secrets in Code**: Never commit API keys, passwords, or other sensitive credentials directly into the codebase. Use environment variables.
8.  **No Commented-Out Code**: Remove dead or commented-out code before committing.
9.  **Keep Dependencies Clean**: Do not add new third-party packages without a valid reason.


---

## Continuous Verification Guideline

After implementing any feature, bug fix, or refactor, you must verify that the system remains stable and correct. Follow these steps to ensure no new issues have been introduced:

1.  **Run All Relevant Tests**: Execute the test suite (`pytest`) to confirm that all existing and new tests pass. This is the primary guard against regressions.
2.  **Perform Static Analysis**: Run any available linting or static analysis tools to check for code quality and style violations.
3.  **Check Build Integrity**: If a build process exists, ensure the application compiles and packages successfully without errors.
4.  **Conduct Impact Analysis**:
    *   Briefly consider the change's potential side effects.
    *   If you modify a shared component (e.g., a domain entity), mentally review the areas that depend on it to ensure they are still compatible.
5.  **Confirm High-Level Functionality**: Before finishing, perform a final "sanity check." Does the feature work as intended? Does the app still run? This confirms that the individual parts integrate correctly.

---

## Output Optimization Guidelines

This section is the canonical source for response verbosity and token efficiency across repository AI setup files.

### Default Verbosity Policy

- **Default mode:** Low verbosity for routine responses.
- **Escalation:** Use Medium only when the task requires extra context for correctness.
- **Deep detail:** Use High only for explicit user requests or complex, high-risk documentation decisions.
- **Rule:** If unsure, start Low and expand only on request.

### Hybrid Token Budgets

- **Default budget:** 200-350 tokens for normal responses.
- **Extended budget:** 500-700 tokens for complex multi-step outputs.
- **Complexity triggers for extended budget (at least one required):**
  - Multi-phase plans with dependencies.
  - Trade-off analysis or decision matrices.
  - User explicitly requests deep detail.

### Response Efficiency Rules

- Prioritize concise bullets and short sections over long prose.
- Avoid repeating repository or conversation context already established.
- Include only critical decisions, actions, risks, and next steps.
- Prefer incremental delivery for long tasks instead of one oversized response.

### Stop/Continue Pattern

- When approaching budget limits, end with a brief checkpoint summary.
- Continue with additional detail only when needed or requested.
- Do not duplicate earlier sections when continuing.


## Code Style Guidelines

### General Guidelines
- Follow clean coding practices.
- Write self-documenting code using descriptive names for variables, functions, and classes.
- Aim to write comments only when the code does not explain itself.

### Formatting
- Use Prettier to format the code:
  ```bash
  npx prettier --write .
  ```
- Configurations include:
  - **Tab Width**: 2 spaces
  - **Quotes**: Use single quotes wherever possible
  - **Line Length**: 80 characters
  - **Semicolons**: Always include

### Imports
- Group imports logically:
  1. Standard libraries (e.g., `fs`, `path`)
  2. Third-party dependencies (alphabetized)
  3. Internal modules (alphabetized by relative path)
- Avoid unused imports.


### Naming Conventions
- **Files/Directories**: Use `kebab-case` for filenames and directories.
- **Variables/Constants**: Use `camelCase`. Constants should use `UPPER_SNAKE_CASE`.
- **Functions**: Use `camelCase` and start function names with a verb (e.g., `getUserData`).
- **Classes**: Use `PascalCase`.

### Error Handling
- Use `try...catch` for asynchronous code whenever necessary.
- Always include error messages and other metadata in logs.
- Avoid exposing raw error data publicly.

---

### Test-Driven Development (TDD)

Please adhere to the following TDD principles when working on this codebase:

1. **Write the Test First**
   - Before implementing new functionality, write a test that specifies and validates what you expect the code to do.

2. **Confirm the Test Fails Initially**
   - Ensure that the test fails when it is first written. This ensures the test is valid and properly reflects the absence of the intended functionality.

3. **Implement the Minimum Code**
   - Write just enough code to make the test pass. Avoid over-engineering or adding unnecessary features.

4. **Refactor the Code**
   - Once the test passes, review and refactor the code to improve structure and readability while ensuring the tests remain green.

5. **Ensure Code is Easy to Test**
   - Write clean, modular, and testable code. Avoid hidden dependencies or tightly coupled logic that makes testing difficult.

---

## Backend Python Agent Guidelines

When working on the FastAPI backend under `src/app/`, adhere to the following Clean Architecture, Domain-Driven Design (DDD), and Python best practices.

### Clean Architecture Principles

1. **Layer Separation**
   - `domain/`: Business entities, value objects, and domain logic (no external dependencies)
   - `application/`: Use cases, DTOs, interfaces for repositories/services
   - `infrastructure/`: External implementations (DB, API clients, file system)
   - `presentation/`: API routes, schemas, FastAPI dependencies

2. **Dependency Rule**
   - Dependencies must point inward. Outer layers depend on inner layers, never the reverse.
   - Use dependency injection to decouple implementations from interfaces.

3. **Single Responsibility**
   - Each module/class should have one reason to change.
   - Keep use cases focused on orchestrating domain logic, not implementing it.

### Domain-Driven Design (DDD) Practices

1. **Bounded Contexts**
   - Group related domain logic into bounded contexts.
   - Each context should have its own models, services, and repository interfaces.

2. **Entities & Value Objects**
   - **Entities**: Objects with a distinct identity that persists over time (e.g., `User`, `Story`)
   - **Value Objects**: Immutable objects defined by their attributes (e.g., `EmailAddress`, `Money`)
   - Use dataclasses or Pydantic models for value objects; ensure immutability.

3. **Aggregates & Aggregate Roots**
   - Define aggregates to group related entities and enforce invariants.
   - The aggregate root is the only entity accessible from outside the aggregate.

4. **Domain Services**
   - Use domain services for operations that don't belong to a single entity.
   - Keep domain services stateless and focused on business rules.

5. **Repository Pattern**
   - Define repository interfaces in `application/` (ports).
   - Implement repositories in `infrastructure/` (adapters).
   - Never leak infrastructure details into the domain layer.

6. **Domain Events**
   - Use domain events for cross-aggregate communication.
   - Implement an event bus for decoupled event handling.

### Python Best Practices

1. **Type Hints**
   - Use full type hints for all function signatures and class attributes.
   - Use `typing.Optional` instead of `| None` for broader compatibility.
   - Use Pydantic for DTOs and request/response models.

2. **Async/Await**
   - Use `async def` for I/O-bound operations (DB, HTTP calls).
   - Use `await` for all async calls; avoid blocking the event loop.
   - Use `run_in_executor` only for CPU-bound operations.

3. **Dataclasses & Pydantic**
   - Use `@dataclass(frozen=True)` for immutable value objects.
   - Use Pydantic `BaseModel` for API schemas and DTOs.
   - Use `BaseModel` with `ConfigDict` for configuration classes.

4. **Error Handling**
   - Define custom exception classes in the domain layer.
   - Use exception hierarchies to categorize errors.
   - Catch exceptions at the appropriate layer; re-raise domain exceptions from infrastructure.

5. **Logging**
   - Use `logging.getLogger(__name__)` for each module.
   - Log at appropriate levels: `DEBUG` for development, `INFO` for significant events, `ERROR` for failures.
   - Include contextual data in log messages using structured logging.

6. **Configuration**
   - Store configuration in `config.py` or `settings.py` using Pydantic `BaseSettings`.
   - Never hardcode configuration values; use environment variables with sensible defaults.
   - Group settings by environment (development, staging, production).

7. **Imports**
   - Follow this import order:
     1. Standard library
     2. Third-party packages
     3. Local application modules (use absolute imports)
   - Avoid circular imports by restructuring dependencies.

8. **Docstrings**
   - Write docstrings for public classes and functions.
   - Use Google-style or NumPy-style docstrings consistently.

### Testing Guidelines

1. **Unit Tests**
   - Test domain logic in isolation using mocks for external dependencies.
   - Use `pytest` and `pytest-asyncio` for testing.
   - Aim for high coverage of domain and application layers.

2. **Integration Tests**
   - Test repository implementations with test databases.
   - Use fixtures for setting up test data.
   - Clean up test data after each test.

3. **API Tests**
   - Use `FastAPI TestClient` for endpoint testing.
   - Test both success and error scenarios.
   - Validate request/response schemas.

### Code Organization

```
src/app/
├── __init__.py
├── main.py                 # FastAPI app initialization
├── config.py               # Application settings
├── domain/
│   ├── __init__.py
│   ├── entities/           # Domain entities
│   ├── value_objects/      # Value objects
│   ├── events/             # Domain events
│   ├── exceptions/         # Custom exceptions
│   └── services/           # Domain services
├── application/
│   ├── __init__.py
│   ├── use_cases/          # Application use cases
│   ├── interfaces/         # Repository/service interfaces
│   └── dtos/               # Data transfer objects
├── infrastructure/
│   ├── __init__.py
│   ├── persistence/        # Database implementations
│   ├── external/          # External service clients
│   └── messaging/         # Event bus implementations
└── presentation/
    ├── __init__.py
    ├── routes/            # API routers
    ├── schemas/           # Pydantic request/response models
    ├── dependencies/     # FastAPI dependencies
    └── middleware/       # Custom middleware
```

---

This document will evolve with the project. Keep it up-to-date as conventions change!
