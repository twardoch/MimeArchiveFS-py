# My Package

`my_package` is a Python project template showcasing a modern development setup using best-in-class tools for dependency management, linting, formatting, testing, and versioning.

## Rationale for Tooling Choices

This project uses a curated set of tools to ensure a high-quality, maintainable, and efficient development experience:

*   **[Hatch](https://hatch.pypa.io/):** A modern, extensible Python project manager. It handles dependency management, virtual environments, building packages, and running scripts.
*   **[uv](https://github.com/astral-sh/uv):** An extremely fast Python package installer and resolver, written in Rust. Hatch can be configured to use `uv` for significantly faster environment setup and dependency installation.
*   **[Ruff](https://github.com/astral-sh/ruff):** An extremely fast Python linter and formatter, written in Rust. It can replace Flake8, isort, Black, and many other tools, providing a unified and very performant experience.
*   **[Mypy](http://mypy-lang.org/):** A static type checker for Python. It helps catch type errors before runtime, improving code reliability.
*   **[Pytest](https://docs.pytest.org/):** A mature and feature-rich testing framework that makes writing tests simple and scalable. Includes support for coverage reporting.
*   **[hatch-vcs](https://github.com/ofek/hatch-vcs):** A Hatch plugin for managing package versions automatically based on Git tags. This simplifies versioning and ensures PEP 440 compliance.
*   **[pre-commit](https://pre-commit.com/):** A framework for managing and maintaining multi-language pre-commit hooks. It helps enforce code quality standards automatically before code is committed.
*   **GitHub Actions:** For continuous integration (CI) to automatically run tests, linters, and type checkers on every push and pull request.

## Features

*   Modern Python packaging with `pyproject.toml`.
*   Project management with Hatch.
*   Fast dependency resolution and installation with `uv` (via Hatch).
*   Comprehensive linting and formatting with Ruff.
*   Static type checking with Mypy.
*   Automated testing with Pytest and code coverage.
*   Automatic versioning based on Git tags using `hatch-vcs`.
*   Pre-commit hooks for automated quality checks.
*   CI setup with GitHub Actions.
*   Source code located in `src/my_package/`.
*   Tests located in `tests/`.

## Installation

### For Users

To install `my_package` as a library in your project:

```bash
pip install my_package
```
(Once the package is published to PyPI. Replace `my_package` with the actual name if different.)

### For Developers

To set up `my_package` for development:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/my_package.git # TODO: Update this URL
    cd my_package
    ```

2.  **Install Hatch:**
    It's recommended to install Hatch using `pipx` for global availability without polluting Python environments:
    ```bash
    pipx install hatch
    ```
    If you don't have `pipx`, install it first (e.g., `python -m pip install --user pipx`).

3.  **Optional: Install uv for faster Hatch operations:**
    For significantly faster environment creation and dependency management with Hatch, install `uv`:
    ```bash
    pipx install uv
    ```
    Then, configure Hatch to use it (this can also be done by setting the `HATCH_UV=1` environment variable):
    ```bash
    hatch config set dirs.env.virtual.uv $(command -v uv)
    ```
    Or, if `uv` is in your PATH, Hatch might pick it up automatically if `HATCH_UV` is set or `uv` support is enabled by default in future Hatch versions.

4.  **Create the development environment:**
    Hatch will create and manage virtual environments for the project.
    ```bash
    hatch env create
    ```
    This command sets up an environment (by default named `default`) with all runtime and development dependencies specified in `pyproject.toml`.

5.  **Activate the development environment:**
    To activate the environment and use the installed tools:
    ```bash
    hatch shell
    ```
    You are now inside the project's virtual environment.

6.  **Install pre-commit hooks:**
    To ensure code quality checks are run automatically before each commit:
    ```bash
    pre-commit install
    ```

## Usage

The main functionality is currently provided by the `hello()` and `add()` functions in `my_package.main`.

```python
from my_package.main import hello, add

print(hello("Developer"))
# Output: Hello, Developer!

result = add(5, 3)
print(f"5 + 3 = {result}")
# Output: 5 + 3 = 8
```

## Development Workflow

This section details how to work on the project, run checks, and manage versions.

### Directory Structure

*   `src/my_package/`: Contains the main source code for the package.
*   `tests/`: Contains all automated tests.
*   `pyproject.toml`: The heart of the project, defining metadata, dependencies, and tool configurations for Hatch, Ruff, Mypy, etc.
*   `.github/workflows/`: Contains GitHub Actions CI configurations.
*   `.pre-commit-config.yaml`: Configuration for pre-commit hooks.

### Running Linters, Formatters, and Type Checkers

We use Hatch scripts to manage quality assurance tasks. These are defined in the `[tool.hatch.envs.lint.scripts]` section of `pyproject.toml`.

*   **To format code and apply auto-fixes (Ruff):**
    ```bash
    hatch run lint:fmt
    ```
    This runs `ruff format .` and `ruff check . --fix`.

*   **To check for linting errors (Ruff) and type errors (Mypy):**
    ```bash
    hatch run lint:check
    ```
    This runs `ruff check .` and `mypy src/my_package/ tests/`.

*   **To run Mypy type checking separately:**
    ```bash
    hatch run lint:mypy
    ```

*   **To run all formatting, linting, and type checking:**
    ```bash
    hatch run lint:style
    ```

Pre-commit hooks will also run many of these checks automatically when you commit changes.

### Running Tests

Tests are written using Pytest and are located in the `tests/` directory.

*   **To run all tests with coverage:**
    ```bash
    hatch run test  # 'test' is an alias for 'default:test'
    ```
    Or explicitly:
    ```bash
    hatch run default:test
    ```
    This command is defined in `[tool.hatch.envs.default.scripts]` in `pyproject.toml` and includes options for coverage reporting (`--cov=src/my_package --cov-report=html --cov-report=xml`) and failing if coverage is below 90% (`--cov-fail-under=90`).

*   **To view the HTML coverage report:**
    After running tests, open `htmlcov/index.html` in your browser.

### Versioning and Releases

This project uses `hatch-vcs` for automatic versioning based on Git tags.

*   **How it works:** The version is dynamically determined from the latest Git tag.
    *   If the current commit is tagged (e.g., `v0.1.0`), that tag is the version.
    *   If there are commits since the last tag, a development version string is generated (e.g., `v0.1.0.post1.dev5+g<hash>`).
*   **Making a release:**
    1.  Ensure your `main` branch is up-to-date and all changes are committed.
    2.  Tag the commit for the release:
        ```bash
        git tag vX.Y.Z  # Replace X.Y.Z with the semantic version (e.g., v0.1.0)
        ```
    3.  Push the tags to the remote repository:
        ```bash
        git push --tags
        ```
    4.  When you build the package (see below), `hatch-vcs` will use this tag as the version.
    A GitHub Action could be set up to automatically build and publish to PyPI when a new tag matching a certain pattern (e.g., `v*.*.*`) is pushed.

### Building the Package

Hatch is used to build the source distribution (sdist) and wheel.

*   **To build the package:**
    ```bash
    hatch build
    ```
    This will create the `sdist` and `wheel` files in the `dist/` directory. These files can then be uploaded to PyPI or another package index.

### Codebase Structure Explanation

*   **`src/my_package/__init__.py`**: Makes `my_package` a Python package. Can also export public symbols.
*   **`src/my_package/main.py`**: Contains the core logic of the package (currently, example functions).
*   **`tests/test_main.py`**: Contains tests for `main.py`. Tests should mirror the structure of the source code.

(This section can be expanded as the codebase grows.)

## Contributing

We welcome contributions! Please follow these guidelines:

1.  Fork the repository on GitHub.
2.  Clone your fork locally.
3.  Set up the development environment as described in the "For Developers" installation section (including `pre-commit install`).
4.  Create a new branch for your feature or bug fix: `git checkout -b my-feature-branch`.
5.  Make your changes. Write clean, well-documented, and well-tested code.
6.  Ensure all quality checks pass:
    *   Pre-commit hooks should pass on commit.
    *   Manually run `hatch run lint:style` and `hatch run test` to be sure.
7.  Commit your changes with clear and descriptive messages.
8.  Push your branch to your fork: `git push origin my-feature-branch`.
9.  Open a pull request against the `main` branch of the original repository. Provide a clear description of your changes.

Please also see the `CONTRIBUTING.md` file for more general contribution etiquette (though most technical details are now in this README).

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
