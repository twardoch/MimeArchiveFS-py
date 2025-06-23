# Contributing

Contributions are welcome! Please follow these guidelines when contributing to this project.

## Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/my_package.git
    cd my_package
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -e .[dev]
    ```

## Running Tests

To run the tests, use pytest:
```bash
pytest
```

## Code Style

This project uses Black for code formatting and Flake8 for linting.

*   **Format code:**
    ```bash
    black .
    ```
*   **Lint code:**
    ```bash
    flake8 .
    ```

## Submitting Changes

1.  Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b my-feature-branch
    ```
2.  Make your changes and commit them with a clear and concise message.
3.  Push your branch to your fork:
    ```bash
    git push origin my-feature-branch
    ```
4.  Open a pull request against the `main` branch of the original repository.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. (TODO: Add a Code of Conduct file)

## Reporting Bugs

If you find a bug, please open an issue on GitHub and provide as much detail as possible, including:
*   Steps to reproduce the bug.
*   Expected behavior.
*   Actual behavior.
*   Your environment (Python version, OS, etc.).

## Suggesting Enhancements

If you have an idea for an enhancement, please open an issue on GitHub to discuss it.
