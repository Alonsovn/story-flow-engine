# AGENTS.md

This guide exists to help agentic tools, like Copilot, operate effectively within this repository. Follow these practices to maintain code quality and consistency while interacting with the project.

---

## Build, Lint, and Test Commands

### Build
Currently, no specific build process is defined. If one becomes necessary, update this section with the appropriate commands. 

### Lint
Ensure code adheres to the repository's coding standards:
```bash
# Lint all files
npx eslint .

# Lint a specific file
npx eslint path/to/file.js
```

### Test
We aim for robust testing practices. Use these commands to run tests:

```bash
# Run all tests
npm test

# Run tests for a specific file or suite:
npm test -- path/to/test.spec.js

# Run a single test
npm test -- -t "Test Name"
```

---

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

### TypeScript (if applicable)
- Always annotate exported functions with explicit types.
- Use interfaces for structure definitions unless type aliases are more appropriate.
- Prefer `unknown` over `any`.
- Type all function parameters and return values.

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

## Continuous Integration (CI)

Ensure all code passes linting and tests before committing:

1. Run all tests:
   ```bash
   npm test
   ```
2. Check formatting and linting:
   ```bash
   npx prettier --check .
   npx eslint .
   ```

---

This document will evolve with the project. Keep it up-to-date as conventions change!
