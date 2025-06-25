# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Generic repository URLs in `pyproject.toml` (`project.urls`).
- `hatch-vcs` to `dependencies` for the `default` environment in `pyproject.toml` to support dynamic versioning during tests.
- `PLAN.md` for tracking project streamlining efforts.
- `TODO.md` for a checklist of project streamlining tasks.
- This `CHANGELOG.md` file.

### Changed
- Corrected `test_add` function in `tests/test_main.py` to properly use parametrized inputs.
- Updated placeholder URLs in `README.md` and `CONTRIBUTING.md` to generic versions.
- Rephrased Code of Conduct section in `CONTRIBUTING.md` to be a note for adopters.
- Corrected typo `skip-magic-trailing_comma` to `skip-magic-trailing-comma` in `[tool.ruff.format]` in `pyproject.toml`.

### Fixed
- **Attempted:** Resolved a persistent `TOMLDecodeError` when parsing `pyproject.toml` by overwriting the file with a known good version. However, the error continues to manifest in the test environment, currently pointing to `pyproject.toml:76:12` (the `]` closing `dependencies` in `[tool.hatch.envs.lint]`). This issue blocks runtime verification of tests and linting configurations via `hatch`.

### Removed
- (None)

### Security
- (None)
