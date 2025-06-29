# My Python Package Template

`my_package` is a modern, comprehensive Python project template designed to kickstart your development with best-in-class tooling and practices already set up. It provides a robust foundation for building scalable and maintainable Python applications and libraries.

## What is `my_package`?

This project serves as a **template** that you can use to create new Python projects. It's not primarily a library to be installed for its own direct functions (like `hello()` or `add()`, which are just examples), but rather a starting point pre-configured with:

*   Dependency management and virtual environments (via Hatch and uv).
*   Linting and formatting (via Ruff).
*   Static type checking (via Mypy).
*   Automated testing (via Pytest with coverage).
*   Automatic versioning based on Git tags (via `hatch-vcs`).
*   Pre-commit hooks for automated code quality checks.
*   A basic CI setup with GitHub Actions.
*   A recommended `src/` layout for cleaner project structure.

## Who is this template for?

This template is for Python developers who want to:

*   Start new projects quickly without spending time on initial setup and configuration of essential tools.
*   Ensure high code quality from the beginning through integrated linting, formatting, and testing.
*   Work with a modern Python development workflow.
*   Learn or demonstrate a setup incorporating current best practices in the Python ecosystem.

## Why is this template useful?

Using this template offers several advantages:

*   **Rapid Project Initialization:** Get a new project up and running in minutes.
*   **Best Practices Included:** Benefit from a curated selection of tools and configurations that promote maintainable and robust code.
*   **Enforced Code Quality:** Integrated linters, formatters, type checkers, and pre-commit hooks help maintain consistency and catch errors early.
*   **Streamlined Workflows:** Hatch scripts simplify common development tasks like running tests, linters, and building the package.
*   **Modern Tooling:** Utilizes fast and efficient tools like Ruff (for linting/formatting) and uv (for package installation).
*   **CI/CD Ready:** Basic GitHub Actions workflow included for automated checks on pushes and pull requests.

## Core Features & Tooling Rationale

This template integrates the following tools and practices, chosen for their effectiveness and modern approach:

*   **[Hatch](https://hatch.pypa.io/):** Manages project environments, dependencies, scripts, and builds. It's extensible and centralizes project management.
*   **[uv](https://github.com/astral-sh/uv):** An extremely fast Python package installer/resolver, written in Rust. Hatch can use `uv` to significantly speed up environment setup and dependency installation.
*   **[Ruff](https://github.com/astral-sh/ruff):** An extremely fast Python linter and formatter, also written in Rust. It replaces multiple tools like Flake8, isort, and Black, offering a unified and performant experience.
*   **[Mypy](http://mypy-lang.org/):** A static type checker for Python, helping to catch type errors before runtime and improve code reliability.
*   **[Pytest](https://docs.pytest.org/):** A mature and feature-rich testing framework that simplifies writing tests and supports comprehensive coverage reporting.
*   **[hatch-vcs](https://github.com/ofek/hatch-vcs):** A Hatch plugin for managing package versions automatically based on Git tags, ensuring PEP 440 compliance and simplifying releases.
*   **[pre-commit](https://pre-commit.com/):** A framework for managing and maintaining multi-language pre-commit hooks, automating quality checks before code is committed.
*   **GitHub Actions:** For continuous integration (CI) to automatically run tests, linters, and type checkers.
*   **`src/` Layout:** Organizes source code in the `src/` directory, distinguishing it from tests and project files.
*   **`pyproject.toml`:** Centralized project configuration following PEP 517, PEP 518, and PEP 621.

## Getting Started with This Template

There are two main ways to use this template:

**1. Using as a GitHub Template:**

   If you are on GitHub, the easiest way is to click the "Use this template" button on the repository page. This will create a new repository in your account with the same files and directory structure.

**2. Cloning Manually:**

   Alternatively, you can clone this repository and then adapt it:
   ```bash
   git clone https://github.com/example-org/example-repo.git your-new-project-name
   cd your-new-project-name
   # Optional: Remove the .git directory to start with a fresh history
   # rm -rf .git
   # git init
   # Add your own remote repository if needed
   # git remote add origin https://github.com/your-username/your-new-project-name.git
   ```

### Initial Configuration for Your New Project

After obtaining the template files, you'll want to customize it:

1.  **Rename the Package:**
    *   The placeholder package name is `my_package`. Decide on your project's actual package name (e.g., `your_actual_package_name`).
    *   Rename the `src/my_package` directory to `src/your_actual_package_name`.
    *   Search and replace `my_package` throughout the codebase, especially in:
        *   `pyproject.toml` (e.g., `project.name`, `tool.ruff.lint.isort.known-first-party`, `tool.hatch.build.targets.wheel.packages`, test paths in scripts like coverage paths).
        *   `tests/` directory and its files (imports, coverage paths).
        *   `src/your_actual_package_name/__init__.py` (if applicable).
        *   `README.md` (this file - update references as needed).
        *   `.github/workflows/main.yml` (paths, package names).

2.  **Update `pyproject.toml`:**
    *   Change `project.name` to `your_actual_package_name`.
    *   Update `project.authors` with your details.
    *   Modify `project.description`.
    *   Review and update `project.urls`.
    *   Adjust `project.requires-python` and `project.classifiers` if needed.
    *   Add your project's runtime dependencies to `project.dependencies`.
    *   Add development-specific dependencies to `project.optional-dependencies.dev`.

3.  **Update Documentation:**
    *   Rewrite this `README.md` to be specific to *your* project. Remove template-specific instructions and fill in details about your actual application/library.
    *   Update `CHANGELOG.md` and other documentation as your project evolves.

4.  **Replace Example Code:**
    *   Delete the example code in `src/your_actual_package_name/main.py`.
    *   Delete the example tests in `tests/test_main.py`.
    *   Start writing your own application logic and tests!

5.  **Initialize Git and Commit (if cloned manually and reset history):**
    ```bash
    # If you ran 'rm -rf .git' and 'git init':
    git add .
    git commit -m "Initial commit from template using my_package"
    # If you haven't already, add a remote and push
    # git remote add origin <your-remote-url>
    # git push -u origin main # or your default branch name
    ```

## Example Code Usage (Illustrative)

The template includes simple example functions `hello()` and `add()` in what would be `src/your_actual_package_name/main.py`. This demonstrates basic structure and testing.

```python
# Assuming your package is named 'your_package_name'
# and you have similar functions after adapting the template.
# from your_package_name.main import hello, add

# print(hello("Developer"))
# # Expected Output: Hello, Developer!

# result = add(5, 3)
# print(f"5 + 3 = {result}")
# # Expected Output: 5 + 3 = 8
```
Remember to replace this with your actual project's functionality and update examples accordingly.

## Command Line Interface (CLI)

This template does not come with a pre-built CLI. However, you can easily add one using libraries like [Click](https://click.palletsprojects.com/) or [Typer](https://typer.tiangolo.com/).

Once you define CLI entry points in your code, you can register them in `pyproject.toml` under `[project.scripts]`:
```toml
[project.scripts]
your-cli-command = "your_package_name.cli:main_function"
```
Hatch will then make `your-cli-command` available in the project's environment. You can also define Hatch scripts in `pyproject.toml` to conveniently run your CLI commands (e.g., `hatch run cli --arg1 value`).

---

## For Developers & Contributors

This section provides technical details about the project structure, development workflow, and contribution guidelines, relevant for those working *on* a project based on this template.

### Project Philosophy

This template is built on the philosophy of using modern, efficient, and well-integrated tools to foster a productive development environment and ensure high code quality. We prioritize:

*   **Clarity and Simplicity:** A straightforward project structure and clear configurations.
*   **Automation:** Automating checks and processes wherever possible (linting, formatting, testing, versioning).
*   **Speed:** Utilizing fast tools like `uv` and `Ruff` to minimize waiting times.
*   **Best Practices:** Adhering to community best practices for Python development.

### Development Environment Setup

To develop a project based on this template:

1.  **Prerequisites:**
    *   **Git:** For version control.
    *   **Python:** Version 3.8+ (as defined in `pyproject.toml`, adjust as needed for your project).
    *   **Hatch:** The project manager. Install via `pipx` for global availability:
        ```bash
        pipx install hatch
        ```
        (If you don't have `pipx`, install it: `python -m pip install --user pipx`).
    *   **Optional but Recommended: `uv`:** For significantly faster Hatch operations:
        ```bash
        pipx install uv
        ```
        Hatch can be configured to use `uv` globally (`hatch config set dirs.env.virtual.uv $(command -v uv)`) or by setting the `HATCH_UV=1` environment variable.

2.  **Clone the Repository:** (If you haven't already)
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

3.  **Create the Development Environment:**
    Hatch manages project-specific virtual environments.
    ```bash
    hatch env create
    ```
    This command creates an environment (default name: `default`) with all runtime and development dependencies from `pyproject.toml`.

4.  **Activate the Environment:**
    ```bash
    hatch shell
    ```
    You are now in the project's virtual environment, with all tools and dependencies available.

5.  **Install Pre-commit Hooks:**
    Automate quality checks before each commit.
    ```bash
    pre-commit install
    ```

### Development Workflow

#### Directory Structure

*   `src/your_package_name/`: Main source code for the package.
*   `tests/`: All automated tests. Test structure should mirror the `src/` structure.
*   `pyproject.toml`: Central configuration file for project metadata, dependencies, Hatch, Ruff, Mypy, etc.
*   `.github/workflows/`: GitHub Actions CI configurations.
*   `.pre-commit-config.yaml`: Configuration for pre-commit hooks.
*   `AGENTS.md`: (If present) Instructions specifically for AI agents working on this codebase.
*   `README.md`: This file (should be adapted for your project).
*   `LICENSE`: Project license.
*   `CONTRIBUTING.md`: General contribution etiquette (points to this README for technical details).

#### Running Linters, Formatters, and Type Checkers

Hatch scripts, defined in `pyproject.toml` (`[tool.hatch.envs.lint.scripts]`), manage quality assurance:

*   **Format code & apply auto-fixes (Ruff):**
    ```bash
    hatch run lint:fmt
    ```
    (Runs `ruff format .` and `ruff check . --fix`)

*   **Check for linting errors (Ruff) & type errors (Mypy):**
    ```bash
    hatch run lint:check
    ```
    (Runs `ruff check .` and `mypy src/your_package_name/ tests/`)

*   **Run all formatting, linting, and type checking:**
    ```bash
    hatch run lint:style
    ```
    (Combines formatting, fixing, linting, and type checking)

*   **Run Mypy separately:** (Useful for pre-commit hooks or specific checks)
    ```bash
    hatch run lint:mypy
    ```

Pre-commit hooks will also run many of these checks automatically on commit.

#### Running Tests

Tests are written using Pytest and located in the `tests/` directory.

*   **Run all tests with coverage:**
    ```bash
    hatch run test  # Alias for 'default:test'
    ```
    Or explicitly:
    ```bash
    hatch run default:test
    ```
    This command (defined in `[tool.hatch.envs.default.scripts]`) runs Pytest, generates coverage reports (HTML and XML), and fails if coverage is below the configured threshold (e.g., 90%). The coverage path (`--cov=src/your_package_name`) needs to be updated if you rename the package.

*   **View HTML Coverage Report:**
    After tests, open `htmlcov/index.html` in a browser.

*   **Running tests for specific Python versions:**
    If matrix environments are defined in `pyproject.toml` (e.g., `tool.hatch.envs.test-py39.matrix`), you can run:
    ```bash
    hatch run test-py39:test # Example for a python3.9 environment
    ```

### Codebase Internals

*   **`pyproject.toml`:**
    *   `[project]`: PEP 621 metadata (name, dynamic version, dependencies, etc.).
    *   `[build-system]`: Specifies Hatchling as the build backend.
    *   `[tool.hatch.version]`: Configures `hatch-vcs` for dynamic versioning from Git tags.
    *   `[tool.hatch.envs.*]`: Defines Hatch environments (like `default`, `lint`) and their scripts and dependencies.
    *   `[tool.ruff]`: Configuration for the Ruff linter and formatter.
    *   `[tool.mypy]`: Configuration for the Mypy static type checker.
*   **`src/your_package_name/__init__.py`:** Makes `your_package_name` a Python package. Can export public symbols.
*   **`src/your_package_name/main.py`:** Contains example logic. Replace with your actual code.
*   **`tests/test_main.py`:** Contains example tests for `main.py`.
*   **`.github/workflows/main.yml`:** Defines the CI pipeline using GitHub Actions. It typically runs linters, type checkers, and tests across different Python versions. Remember to update package paths here if you rename `my_package`.
*   **`.pre-commit-config.yaml`:** Defines hooks that run before commits (e.g., Ruff, Mypy).

### Coding and Contribution Guidelines

#### Coding Standards

*   **Formatting:** Code is formatted with Ruff (`ruff format .`).
*   **Linting:** Adhere to rules enforced by Ruff (`ruff check .`). Configurations are in `pyproject.toml`.
*   **Type Hinting:** Use type hints for all function signatures and strive for comprehensive type coverage. Mypy (`mypy src/your_package_name/ tests/`) is used for static type checking.
*   **Docstrings:** Write clear and concise docstrings for modules, classes, functions, and methods, following standard conventions (e.g., Google style, NumPy style, or reStructuredText).
*   **Modularity:** Design components to be modular and reusable.
*   **Error Handling:** Implement robust error handling using specific exception types.

#### Testing

*   Write tests for all new features and bug fixes in the `tests/` directory.
*   Aim for high test coverage (target: 90%, see `pyproject.toml` under `hatch run test` script).
*   Ensure all tests pass before submitting contributions.

#### Commit Messages

*   Write clear and concise commit messages.
*   Consider following the [Conventional Commits](https://www.conventionalcommits.org/) specification for structured messages. Example:
    ```
    feat: Add user authentication feature

    Implement password hashing and token generation.
    Fixes #123
    ```

#### Pre-commit Hooks

*   Ensure pre-commit hooks are installed (`pre-commit install`).
*   Hooks will automatically run on `git commit` to format code, check for linting issues, and perform other checks. Address any issues reported by the hooks.

#### Versioning and Releases

This project uses `hatch-vcs` for dynamic versioning based on Git tags.

*   **How it works:** The version is derived from the latest Git tag (e.g., `v0.1.0`). Commits after a tag result in development versions (e.g., `v0.1.0.post1.dev5+g<hash>`).
*   **Making a release:**
    1.  Ensure the main branch is up-to-date and all changes are committed.
    2.  Tag the commit: `git tag vX.Y.Z` (e.g., `v0.1.0`).
    3.  Push tags: `git push --tags`.
    A GitHub Action can be set up to automatically build and publish to PyPI when a new version tag is pushed.

#### Building the Package

Hatch builds the source distribution (sdist) and wheel.

*   **To build:**
    ```bash
    hatch build
    ```
    Output is in the `dist/` directory. These files can be uploaded to PyPI.

#### Contributing Process

We welcome contributions to projects based on this template!

1.  **Discuss:** For new features or significant changes, please open an issue first to discuss your ideas.
2.  **Fork & Clone:** Fork the repository on GitHub and clone your fork locally.
3.  **Branch:** Create a new branch for your feature or bug fix: `git checkout -b your-feature-branch`.
4.  **Develop:**
    *   Set up the development environment (see above).
    *   Implement your changes, adhering to coding standards and writing tests.
5.  **Test & Lint:** Ensure all checks pass:
    *   `hatch run lint:style` (or the more specific `lint:fmt` and `lint:check`)
    *   `hatch run test`
    *   Pre-commit hooks should pass on commit.
6.  **Commit & Push:** Commit your changes with clear messages and push to your fork.
7.  **Pull Request:** Open a pull request (PR) against the `main` branch of the upstream repository.
    *   Provide a clear description of your changes and link any relevant issues.

Please also refer to `CONTRIBUTING.md` for general contribution etiquette and any project-specific Code of Conduct.

### License

This project (and the template itself) is licensed under the Apache License 2.0. See the `LICENSE` file for details.
