# Release Guide

## Overview

This project now includes a complete git-tag-based semversioning system with automated CI/CD pipelines and binary distribution capabilities.

## Features Implemented

### ✅ Git-Tag-Based Semversioning
- **Version Source**: `hatch-vcs` automatically determines version from git tags
- **Tag Format**: `vX.Y.Z` (e.g., `v1.0.0`, `v2.1.3`)
- **Development Versions**: Automatic `.post.dev` versions between tags
- **Regex Validation**: Ensures tags follow semantic versioning

### ✅ Comprehensive Test Suite
- **Main Tests**: Core functionality testing with edge cases
- **Package Tests**: Import and structure validation
- **Integration Tests**: Build system and tool integration
- **Coverage**: 90% minimum coverage requirement
- **Platforms**: Tests run on Linux, macOS, and Windows

### ✅ Local Scripts
- **`scripts/dev-setup.sh`**: Complete development environment setup
- **`scripts/test.sh`**: Run all tests with linting and formatting
- **`scripts/build.sh`**: Build Python packages (wheel and sdist)
- **`scripts/release.sh`**: Interactive release process with git tagging

### ✅ GitHub Actions CI/CD
- **Main Pipeline**: Tests on multiple Python versions and platforms
- **Release Pipeline**: Automated releases on git tags
- **Binary Pipeline**: Standalone executable builds
- **Artifact Management**: Automatic upload and distribution

### ✅ Multiplatform Support
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Operating Systems**: Ubuntu, macOS, Windows
- **Architectures**: x86_64, ARM64 (macOS)

### ✅ Binary Artifacts
- **Standalone Executables**: PyInstaller-based binaries
- **Platform Coverage**: Linux, macOS (x86_64 + ARM64), Windows
- **CLI Interface**: Command-line interface for main functionality
- **Distribution**: Automatic GitHub release attachment

## Quick Start

1. **Development Setup**:
   ```bash
   ./scripts/dev-setup.sh
   ```

2. **Run Tests**:
   ```bash
   ./scripts/test.sh
   ```

3. **Build Package**:
   ```bash
   ./scripts/build.sh
   ```

4. **Create Release**:
   ```bash
   ./scripts/release.sh
   ```

## Release Process

### Automated (Recommended)

1. Use the release script:
   ```bash
   ./scripts/release.sh
   ```

2. Follow the prompts to:
   - Verify you're on main branch
   - Run all tests
   - Build the package
   - Create and push a git tag

3. GitHub Actions will automatically:
   - Run tests on all platforms
   - Create GitHub release
   - Build and upload Python packages
   - Build and upload binary executables
   - Publish to PyPI (if configured)

### Manual Process

```bash
# 1. Ensure everything is committed and pushed
git status
git push origin main

# 2. Run tests
./scripts/test.sh

# 3. Build package
./scripts/build.sh

# 4. Create and push tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will handle the rest
```

## Installation Options

### Python Package (PyPI)
```bash
pip install my-package
```

### Binary Downloads
Download platform-specific binaries from GitHub releases:
- **Linux**: `my-package-linux-x86_64`
- **macOS (Intel)**: `my-package-macos-x86_64`  
- **macOS (Apple Silicon)**: `my-package-macos-arm64`
- **Windows**: `my-package-windows-x86_64.exe`

### Usage
```bash
# Python package
python -m my_package

# Binary
./my-package-linux-x86_64 hello "World"
./my-package-linux-x86_64 add 5 3
```

## Version Management

### Version Determination
- **Tagged Commits**: Exact version from tag (e.g., `1.0.0`)
- **Development**: Auto-generated with commit info (e.g., `1.0.0.post1.dev5+g<hash>`)
- **Clean Working Directory**: Required for releases

### Tag Format
- **Valid**: `v1.0.0`, `v2.1.3`, `v10.0.0`
- **Invalid**: `1.0.0`, `v1.0`, `v1.0.0-alpha`

### Example Version History
```
v0.1.0 → 0.1.0 (initial release)
      → 0.1.0.post1.dev1+g<hash> (development)
      → 0.1.0.post1.dev2+g<hash> (more development)
v0.2.0 → 0.2.0 (next release)
```

## GitHub Actions Workflows

### 1. Main CI/CD (`.github/workflows/main.yml`)
- **Trigger**: Push to main, pull requests
- **Matrix**: Python 3.8-3.12 × Ubuntu/macOS/Windows
- **Steps**: Lint, test, build, upload artifacts

### 2. Release (`.github/workflows/release.yml`)
- **Trigger**: Git tags matching `v*`
- **Steps**: Test, build, create GitHub release, publish to PyPI

### 3. Binaries (`.github/workflows/binaries.yml`)
- **Trigger**: Git tags matching `v*`
- **Platforms**: Linux, macOS (x86_64 + ARM64), Windows
- **Output**: Standalone executables with checksums

## Configuration Files

### Core Configuration
- **`pyproject.toml`**: Project metadata, dependencies, tool configuration
- **`.pre-commit-config.yaml`**: Code quality automation
- **`.github/workflows/`**: CI/CD pipeline definitions

### Development Tools
- **Ruff**: Linting and formatting
- **Mypy**: Static type checking
- **Pytest**: Testing framework
- **Hatch**: Build system and environment management
- **Pre-commit**: Git hook automation

## Troubleshooting

### Common Issues

1. **Version not updating**: Check git tags and fetch from remote
2. **Tests failing**: Ensure all dependencies are installed
3. **Build errors**: Verify `pyproject.toml` configuration
4. **CI failures**: Check GitHub Actions logs for details

### Debug Commands
```bash
# Check version
hatch version

# List environments
hatch env show

# Check git tags
git tag --list

# Validate configuration
hatch config show
```

## Next Steps

1. **Configure PyPI Publishing**:
   - Set up PyPI trusted publishing
   - Add repository secrets if needed

2. **Customize Binary Distribution**:
   - Modify `cli/main.py` for your use case
   - Update binary build configuration

3. **Enhance Documentation**:
   - Add API documentation
   - Create user guides
   - Update README with installation instructions

4. **Monitor Releases**:
   - Set up notifications for failed builds
   - Monitor PyPI download statistics
   - Track GitHub release metrics

## Support

For issues or questions:
1. Check the `DEVELOPMENT.md` guide
2. Review GitHub Actions logs
3. Consult the `README.md` for basic usage
4. Open an issue on GitHub

---

🎉 **Congratulations!** Your project now has a complete, automated release pipeline with git-tag-based semversioning and multiplatform binary distribution.