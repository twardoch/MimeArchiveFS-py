# Development Guide

This document provides comprehensive instructions for developing, testing, and releasing this package.

## Quick Start

1. **Set up development environment:**
   ```bash
   ./scripts/dev-setup.sh
   ```

2. **Run tests:**
   ```bash
   ./scripts/test.sh
   ```

3. **Build package:**
   ```bash
   ./scripts/build.sh
   ```

4. **Create a release:**
   ```bash
   ./scripts/release.sh
   ```

## Development Environment Setup

### Prerequisites

- Python 3.8+
- Git
- Optional: `pipx` for global tool installation

### Initial Setup

The `./scripts/dev-setup.sh` script will:
- Install `hatch` and `uv` via `pipx`
- Configure `hatch` to use `uv` for faster dependency resolution
- Create the development environment
- Install pre-commit hooks
- Make all scripts executable

### Manual Setup

If you prefer manual setup:

```bash
# Install hatch and uv
pipx install hatch
pipx install uv

# Configure hatch to use uv
hatch config set dirs.env.virtual.uv $(command -v uv)

# Create development environment
hatch env create

# Install pre-commit hooks
hatch run pre-commit install
```

## Development Workflow

### Code Quality

This project uses several tools to ensure code quality:

- **Ruff**: Fast Python linter and formatter
- **Mypy**: Static type checker
- **Pytest**: Testing framework with coverage
- **Pre-commit**: Automated quality checks

### Running Quality Checks

```bash
# Format code and apply auto-fixes
hatch run lint:fmt

# Check for linting errors and type errors
hatch run lint:check

# Run comprehensive style checks
hatch run lint:style

# Run tests with coverage
hatch run test
```

### Pre-commit Hooks

Pre-commit hooks run automatically on every commit:

- Code formatting (Ruff)
- Linting (Ruff)
- Type checking (Mypy)
- Various file checks (trailing whitespace, YAML validation, etc.)

To run pre-commit on all files:
```bash
hatch run pre-commit run --all-files
```

## Testing

### Test Structure

```
tests/
├── test_main.py          # Main functionality tests
├── test_package.py       # Package structure tests
└── test_integration.py   # Integration tests
```

### Running Tests

```bash
# Run all tests with coverage
./scripts/test.sh

# Or manually
hatch run test

# Run specific test file
hatch run pytest tests/test_main.py

# Run with verbose output
hatch run pytest -v
```

### Test Coverage

The project maintains 90% test coverage. Coverage reports are generated in:
- `htmlcov/index.html` (HTML report)
- `coverage.xml` (XML report for CI)

## Building and Packaging

### Local Build

```bash
# Build package
./scripts/build.sh

# Or manually
hatch build
```

This creates:
- `dist/*.whl` - Python wheel for installation
- `dist/*.tar.gz` - Source distribution

### Binary Build

To build standalone binaries:

```bash
# Install PyInstaller
hatch run pip install pyinstaller

# Build binary
hatch run pyinstaller --onefile --name my-package cli/main.py
```

## Release Process

### Git Tag-based Versioning

This project uses `hatch-vcs` for automatic versioning based on Git tags:

- Tags must follow semantic versioning: `vX.Y.Z` (e.g., `v1.0.0`)
- Version is automatically determined from the latest Git tag
- Development versions include commit info: `v1.0.0.post1.dev5+g<hash>`

### Creating a Release

1. **Ensure main branch is clean:**
   ```bash
   git status
   git push origin main
   ```

2. **Run the release script:**
   ```bash
   ./scripts/release.sh
   ```

   This script will:
   - Check you're on the main branch
   - Verify working directory is clean
   - Run all tests
   - Build the package
   - Prompt for the new version tag
   - Create and push the git tag

3. **GitHub Actions will automatically:**
   - Run tests on all platforms
   - Build the package
   - Create a GitHub release
   - Upload build artifacts
   - Build standalone binaries
   - Publish to PyPI (if configured)

### Manual Release Steps

If you prefer manual control:

```bash
# Run tests
./scripts/test.sh

# Build package
./scripts/build.sh

# Create and push tag
git tag v1.0.0
git push origin v1.0.0
```

## Continuous Integration

### GitHub Actions Workflows

1. **Main CI/CD Pipeline** (`.github/workflows/main.yml`)
   - Runs on push and pull requests
   - Tests on multiple Python versions and platforms
   - Builds and uploads artifacts

2. **Release Pipeline** (`.github/workflows/release.yml`)
   - Triggered by git tags
   - Creates GitHub releases
   - Publishes to PyPI

3. **Binary Builds** (`.github/workflows/binaries.yml`)
   - Builds standalone executables
   - Supports Linux, macOS, and Windows

### Supported Platforms

- **Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Operating systems**: Ubuntu, macOS, Windows
- **Architectures**: x86_64, ARM64 (macOS)

## Configuration Files

### `pyproject.toml`

Central configuration file containing:
- Project metadata
- Build system configuration
- Tool configurations (Ruff, Mypy, Pytest)
- Hatch environments and scripts

### `.pre-commit-config.yaml`

Pre-commit hooks configuration:
- File format checks
- Code formatting and linting
- Type checking

### GitHub Actions

- `.github/workflows/main.yml` - Main CI/CD pipeline
- `.github/workflows/release.yml` - Release automation
- `.github/workflows/binaries.yml` - Binary builds

## Troubleshooting

### Common Issues

1. **Hatch environment issues:**
   ```bash
   # Remove and recreate environment
   hatch env remove
   hatch env create
   ```

2. **Pre-commit hook failures:**
   ```bash
   # Update pre-commit hooks
   hatch run pre-commit autoupdate
   
   # Run pre-commit manually
   hatch run pre-commit run --all-files
   ```

3. **Version not updating:**
   ```bash
   # Check git tags
   git tag --list
   
   # Fetch tags from remote
   git fetch --tags
   ```

### Getting Help

- Check the README.md for basic usage
- Review the GitHub Actions logs for CI failures
- Ensure all dependencies are installed correctly
- Verify git tags are properly formatted (`vX.Y.Z`)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `./scripts/test.sh`
5. Commit your changes (pre-commit hooks will run)
6. Push to your fork
7. Create a pull request

All contributions must pass the CI pipeline and maintain test coverage.