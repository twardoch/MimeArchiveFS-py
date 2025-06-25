# Project Streamlining TODO List

- [x] **Project Setup & Analysis**
  - [x] Generate `llms.txt` if it doesn't exist.
  - [x] Analyze `llms.txt` and project structure for MVP streamlining.
- [x] **Refine Test Implementation**
  - [x] Correct `test_add` in `tests/test_main.py` to use parametrized inputs.
  - [ ] Verify test fix by running `hatch run test`. (Blocked by `pyproject.toml` parsing issue)
  - [x] Add `hatch-vcs` to `[tool.hatch.envs.default.dependencies]` in `pyproject.toml`.
- [x] **Update Configuration Files**
  - [x] In `pyproject.toml`:
    - [x] Replace placeholder URLs in `[project.urls]` with generic ones.
    - [x] Correct typo `skip-magic-trailing_comma` to `skip-magic-trailing-comma`.
  - [ ] Verify `pyproject.toml` functionality. (Blocked by `pyproject.toml` parsing issue)
- [x] **Update Documentation**
  - [x] In `README.md`:
    - [x] Replace placeholder clone URL with a generic version.
  - [x] In `CONTRIBUTING.md`:
    - [x] Replace placeholder clone URL with a generic one for user forks.
    - [x] Rephrase Code of Conduct TODO to a note for adopters.
- [ ] **Create Planning and Tracking Documents**
  - [x] Create `PLAN.md` with the detailed plan.
  - [x] Create `TODO.md` (this file).
  - [ ] Create and initialize `CHANGELOG.md`, then update with progress.
- [ ] **Implement Changes & Document Progress** (Meta-step, progress tracked via other items)
- [ ] **Review and Finalize**
  - [ ] Review all code, configuration, and documentation changes.
  - [ ] Ensure all documentation files are consistent and up-to-date.
  - [ ] Attempt to run all quality checks (`hatch run lint:style`, `hatch run test`). (Blocked by `pyproject.toml` parsing issue)
- [ ] **Submit Changes**
  - [ ] Commit all changes with a descriptive message.
  - [ ] Use an appropriate branch name.

**Persistent Blocker:**
- [ ] Resolve `TOMLDecodeError` when `hatch` parses `pyproject.toml`. Current error points to `pyproject.toml:76:12` (the `]` closing `dependencies` in `[tool.hatch.envs.lint]`). This prevents full verification of tests and configurations.Tool output for `create_file_with_block`:
