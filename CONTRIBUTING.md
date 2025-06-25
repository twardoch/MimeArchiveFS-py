# Contributing

Thank you for considering contributing to `my_package`! We welcome all contributions, from bug reports and documentation improvements to new features.

## Getting Started

1.  **Familiarize yourself with the project:** Please read the main `README.md` file thoroughly. It contains:
    *   An overview of the project and its goals.
    *   Detailed instructions for setting up your development environment (using Hatch, uv, pre-commit, etc.).
    *   Guidance on running linters, formatters, type checkers, and tests.
    *   Information about our versioning and release process.
    *   An explanation of the codebase structure.

2.  **Find an issue or suggest an idea:** Check the issue tracker on GitHub for existing bugs, feature requests, or discussions. If you have a new idea or want to work on something not listed, please open an issue first to discuss it with the maintainers.

## Contribution Workflow

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/YOUR_USERNAME/example-repo.git # Replace YOUR_USERNAME with your GitHub username
    cd example-repo # Or your chosen directory name
    ```
3.  **Set up your development environment** by following the instructions in the "For Developers" section of `README.md`. This includes installing Hatch, creating the environment with `hatch env create`, and installing pre-commit hooks with `pre-commit install`.
4.  **Create a new branch** for your changes:
    ```bash
    git checkout -b your-descriptive-branch-name
    ```
5.  **Make your changes.** Ensure you write clean, well-documented, and well-tested code.
6.  **Run all quality checks** as described in the `README.md` (e.g., `hatch run lint:style`, `hatch run test`). Pre-commit hooks will help, but a full manual check is also recommended.
7.  **Commit your changes** with clear and concise commit messages. Consider following conventional commit formats if you are familiar with them.
    ```bash
    git commit -m "feat: Add new feature X" -m "Detailed description of changes."
    ```
8.  **Push your branch** to your fork:
    ```bash
    git push origin your-descriptive-branch-name
    ```
9.  **Open a Pull Request (PR)** against the `main` branch of the original `my_package` repository.
    *   Provide a clear title and description for your PR.
    *   Link to any relevant issues.
    *   Explain your changes and why they are needed.

## Code of Conduct

This project and everyone participating in it is governed by a Code of Conduct. (Note: If you adopt this project, please create a `CODE_OF_CONDUCT.md` file and link to it here, or remove/rephrase this section as appropriate.) By participating, you are expected to uphold this code. Please report unacceptable behavior.

## Reporting Bugs

If you encounter a bug, please open an issue on GitHub. Include:
*   A clear and descriptive title.
*   Steps to reproduce the bug.
*   What you expected to happen.
*   What actually happened (including any error messages or tracebacks).
*   Your environment (e.g., Python version, OS, `my_package` version, Hatch version).

## Suggesting Enhancements

If you have an idea for an enhancement, please open an issue on GitHub. Provide:
*   A clear and descriptive title.
*   A detailed explanation of the proposed enhancement.
*   The motivation or use case for this enhancement.
*   Any potential drawbacks or alternative solutions.

We appreciate your contributions to making `my_package` better!
