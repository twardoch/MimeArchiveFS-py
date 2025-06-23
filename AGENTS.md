# Agent Instructions

This document provides instructions for AI agents working with this codebase.

## Project Overview

This is a Python package managed with Hatch. It includes:
- Source code in `src/my_package/`
- Tests in `tests/`
- Dependency management with `pyproject.toml` (using Hatch and uv for faster environment setup)
- Linting with Ruff (to be configured)
- Formatting with Ruff (to be configured, replacing Black)
- Type checking with Mypy
- Testing with Pytest (including coverage)
- Versioning with `hatch-vcs` based on Git tags
- CI/CD with GitHub Actions
- Pre-commit hooks for automated checks (to be configured)

## Development Workflow

When making changes, please adhere to the following:

1.  **Understand the requirements:** Ensure you have a clear understanding of the task.
2.  **Set up the environment:** Use `hatch env create` to set up your development environment. Activate it with `hatch shell`. For faster setup, ensure `uv` is available or set `HATCH_UV=1`.
3.  **Write tests:** For new features or bug fixes, write tests first or alongside the implementation. Aim for high test coverage.
4.  **Implement the code:** Write clean, maintainable, and well-documented code in `src/my_package/`.
5.  **Run linters, formatters, and type checkers:**
    Use Hatch scripts (to be fully configured with Ruff). For example:
    ```bash
    hatch run lint:style  # Will run Ruff format, Ruff lint, Mypy
    hatch run lint:fmt    # For formatting only (with Ruff)
    hatch run lint:check  # For linting and type checking only (Ruff, Mypy)
    ```
    Ensure all checks pass. (These scripts will be defined in `pyproject.toml`)
6.  **Run tests:**
    ```bash
    hatch run test
    ```
    Or, to run tests for specific Python versions defined in `tool.hatch.envs.<env_name>.matrix`:
    ```bash
    hatch run python<version>:test
    ```
    Ensure all tests pass and coverage targets are met (currently 90%, configured in `pyproject.toml`'s default env scripts).
7.  **Update documentation:** If your changes affect how the code is used or its external behavior, update `README.md` and any relevant docstrings.
8.  **Commit messages:** Follow conventional commit message formats if possible, or at least provide a clear and concise summary of the changes. Pre-commit hooks will help ensure code quality before committing.

## Important Files

-   `pyproject.toml`: Project metadata, dependencies, Hatch configurations (environments, build, versioning, tools like Ruff, Mypy).
-   `src/my_package/`: Main application/library code.
-   `tests/`: Unit and integration tests.
-   `.github/workflows/main.yml`: GitHub Actions CI configuration (will be updated to use Hatch).
-   `README.md`: Project overview, user-facing documentation, and detailed contribution guidelines.
-   `CONTRIBUTING.md`: High-level guidelines for human contributors, pointing to `README.md` for setup.
-   `LICENSE`: Project license (Apache 2.0).
-   `.pre-commit-config.yaml`: Configuration for pre-commit hooks (to be added).

## Specific Instructions

-   **Dependencies:** Add new runtime dependencies to the `project.dependencies` section in `pyproject.toml`. Add development dependencies to `project.optional-dependencies.dev` and ensure they are included in relevant Hatch environments (e.g., `default`, `lint`).
-   **Type Hinting:** Use type hints for all function signatures and strive for good type coverage. Mypy will be configured to check `src/my_package/`.
-   **Error Handling:** Implement robust error handling. Use specific exception types where appropriate.
-   **Modularity:** Design components to be modular and reusable.
-   **Security:** Be mindful of security best practices, especially if dealing with user input or external services.

By following these guidelines, you will help maintain the quality and consistency of the codebase.
