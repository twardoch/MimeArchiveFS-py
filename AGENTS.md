# Agent Instructions

This document provides instructions for AI agents working with this codebase.

## Project Overview

This is a Python package initialized with a modern project structure. It includes:
- Source code in `src/`
- Tests in `tests/`
- Dependency management with `pyproject.toml` (using setuptools and pip)
- Linting with Flake8
- Formatting with Black
- Type checking with Mypy
- Testing with Pytest (including coverage)
- CI/CD with GitHub Actions

## Development Workflow

When making changes, please adhere to the following:

1.  **Understand the requirements:** Ensure you have a clear understanding of the task.
2.  **Write tests:** For new features or bug fixes, write tests first or alongside the implementation. Aim for high test coverage.
3.  **Implement the code:** Write clean, maintainable, and well-documented code.
4.  **Run linters and formatters:**
    ```bash
    black .
    flake8 .
    mypy src/
    ```
    Ensure all checks pass.
5.  **Run tests:**
    ```bash
    pytest
    ```
    Ensure all tests pass and coverage targets are met (currently 90%).
6.  **Update documentation:** If your changes affect how the code is used or its external behavior, update `README.md` and any relevant docstrings.
7.  **Commit messages:** Follow conventional commit message formats if possible, or at least provide a clear and concise summary of the changes.

## Important Files

-   `pyproject.toml`: Project metadata and dependencies. Add new dependencies here.
-   `src/`: Main application/library code.
-   `tests/`: Unit and integration tests.
-   `pytest.ini`: Pytest configuration.
-   `.flake8`: Flake8 configuration.
-   `.github/workflows/main.yml`: GitHub Actions CI configuration.
-   `README.md`: Project overview and user-facing documentation.
-   `CONTRIBUTING.md`: Guidelines for human contributors.
-   `LICENSE`: Project license (Apache 2.0).

## Specific Instructions

-   **Dependencies:** Add new runtime dependencies to the `project.dependencies` section in `pyproject.toml` and development dependencies to `project.optional-dependencies.dev`.
-   **Type Hinting:** Use type hints for all function signatures and strive for good type coverage. Mypy is configured to check `src/`.
-   **Error Handling:** Implement robust error handling. Use specific exception types where appropriate.
-   **Modularity:** Design components to be modular and reusable.
-   **Security:** Be mindful of security best practices, especially if dealing with user input or external services.

By following these guidelines, you will help maintain the quality and consistency of the codebase.
