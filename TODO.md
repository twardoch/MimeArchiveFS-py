# MimeArchiveFS-py (`mimearchivefs`) Specification & Skeleton

This document outlines the specification and proposed project structure for the `mimearchivefs` Python package, designed to implement a virtual filesystem based on an MHTML-compatible single-file archive format (`.mht`). 

## 1. Next Steps (High-Level)

- [x] 1. Complete project structure setup (create `src/mimearchivefs`, `pyproject.toml`, `README.md`, etc.).
- [x] 2. Configure `pyproject.toml` (dependencies, linters, build tool - e.g., hatch/uv).
- [x] 3. Implement helper functions in `src/mimearchivefs/utils.py` (tests in `tests/test_utils.py` exist).
- [x] 4. Implement basic parsing logic in `src/mimearchivefs/core.py` using `email.parser`.
- [x] 5. Implement read-only `MimeArchiveFileSystem` in `src/mimearchivefs/filesystem.py`, leveraging `core.py` and `utils.py`.
- [x] 6. Write tests for `core.py` and `filesystem.py` (read operations). Use `fsspec` test suite.
- [x] 7. Set up CI (`.github/workflows/ci.yml`) and pre-commit hooks (`.pre-commit-config.yaml`).
- [x] 8. Write basic `README.md` and initial usage docs.
- [x] 9. Implement write operations and associated tests.
- [ ] 11. Implement archive API (`src/mimearchivefs/archive.py`) that mimics Python's `zipfile` standard library.
    - [ ] `MimeArchive` class similar to `ZipFile`
    - [ ] `MimeArchiveInfo` class similar to `ZipInfo`
    - [ ] Compatibility methods: `namelist()`, `infolist()`, `extract()`, `extractall()`, etc.
- [ ] 10. Implement CLI (`src/mimearchivefs/cli.py`) and tests (`tests/test_cli.py`).
    - [ ] Basic commands: list, extract, create, append, info
    - [ ] Advanced: mount functionality using `fsspec`
- [ ] 12. Ensure full fsspec compatibility for all operations.
    - [ ] Add comprehensive tests against fsspec test suite
    - [ ] Fix any compatibility issues
    - [ ] Document all supported operations
- [ ] 13. Set up documentation framework (Sphinx/MkDocs).
    - [ ] API reference
    - [ ] Usage examples
    - [ ] CLI documentation
- [ ] 14. Create example usage scripts (`examples/`).
    - [ ] Basic usage examples
    - [ ] Examples for all three APIs: fsspec, archive, and CLI
- [ ] 15. Create `CHANGELOG.md` and `NOTES.md`.
- [ ] 16. Create test fixtures (`tests/fixtures/*.mht`).
- [x] 17. Implement `src/mimearchivefs/exceptions.py`.
- [x] 18. Add `src/mimearchivefs/__init__.py` exports.
- [ ] 19. Add performance benchmarks and optimizations.
- [ ] 20. Create comprehensive documentation website.




## 2. General Guidelines

### 2.1. Introduction

MimeArchiveFS-py ("MAFS") is the Python implementation of a virtual filesystem built around a mountable single-file archive format that extends MHTML and is backwards-compatible to it. 

A MimeArchiveFS archive (container, MIME type `application/x-mimearchive`) is a file with the extension `.mht`, which acts as a universal container for multiple plaintext and binary files, making it ideal for packaging code repositories, markdown files, and even configuration data into a structured yet easily accessible format. The core idea revolves around defining MIME-like boundaries within a plain text document, where each file entry is separated by a `--- FILE: folder/folder/filename ---` marker, followed by its raw content if it's plaintext or base64-encoded binary if necessary. 

This ensures full backwards compatibility with MHTML, meaning existing tools capable of parsing MIME-based multipart files can handle extraction effortlessly. A FUSE-compatible filesystem driver allows seamless mounting of the archive as a virtual directory, enabling applications and operating systems to interact with its contents as if they were normal files without requiring extraction. 

This is highly advantageous for AI and LLM contexts, where structured multi-file inputs are required, allowing models to ingest bundled repositories, project documentation, or structured datasets without dealing with fragmented inputs. Additionally, since the archive remains human-readable, developers can manually inspect or manipulate the stored files without specialized tooling, ensuring both transparency and ease of adoption. 

This approach, combining structured file storage, efficient binary handling, and OS-level accessibility, could make virtualized text-based archives a practical alternative to conventional `.zip` or `.tar` formats while maintaining simplicity and readability. 

We want a MimeArchiveFS implementation written in Python based on the `fsspec` package, modeled after, and possibly re-using some part of, [fsspec.implementations.memory](https://filesystem-spec.readthedocs.io/en/latest/_modules/fsspec/implementations/memory.html) and/or [fsspec.implementations.zip.ZipFileSystem](https://filesystem-spec.readthedocs.io/en/latest/_modules/fsspec/implementations/zip.html)

### 2.2. Core Concept

-   **Format:** A single `.mht` file containing multiple files.
-   **Structure:** Uses MIME multipart structure (`multipart/mixed` or similar).
-   **File Delimiter:** Each file entry is marked by a distinct boundary, potentially incorporating a `--- FILE: path/to/file ---` marker within a header or the part itself for easy identification.
-   **Encoding:** Plaintext files stored as-is (UTF-8 preferred). Binary files encoded using Base64.
-   **Compatibility:** Backwards-compatible with standard MHTML parsers. Filesystem access provided via `fsspec`.

### 2.3. Core Functionality

-   **Parsing:** Read and parse `.mht` files into an internal representation (e.g., a dictionary mapping paths to content/metadata).
-   **fsspec Interface:** Implement `fsspec.spec.AbstractFileSystem` (`MimeArchiveFileSystem`).
-   **Read Operations:**
    -   List directory contents (`ls`).
    -   Get file status/metadata (`info`).
    -   Read file content (`open`, `cat_file`).
    -   Check existence (`exists`).
-   **Write Operations:**
    -   Create/overwrite files (`pipe_file`, `put_file`).
    -   Remove files/directories (`rm_file`, `rmdir`).
    -   Create directories (`mkdir`).
    -   Save changes back to the `.mht` file or a new file (`save`).
-   **ZipFile-like API:**
    -   Functions and classes that mimic Python's standard library `zipfile` module.
    -   Familiar interface for users already accustomed to working with archive files.
-   **CLI Interface:**
    -   Basic file operations (list, extract, create, append).
    -   Mounting the archive as a filesystem using FUSE.
-   **Metadata:** Store basic file metadata (name, size, potentially modification time if feasible within the format).

### 2.4. Proposed Project Structure

```
mimearchivefs/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions for testing, linting, publishing
├── .gitignore
├── .pre-commit-config.yaml  # Pre-commit hooks (ruff, mypy, etc.)
├── CHANGELOG.md
├── LICENSE
├── NOTES.md                 # Developer notes (like the source for this spec)
├── README.md                # Project overview, usage, installation
├── TODO.md                  # This file
├── docs/                    # Documentation (Sphinx or MkDocs)
│   ├── api.md
│   ├── conf.py              # (if Sphinx)
│   ├── index.md
│   ├── make.bat             # (if Sphinx)
│   ├── Makefile             # (if Sphinx)
│   └── usage.md
├── examples/
│   └── basic_usage.py       # Example scripts demonstrating usage
├── pyproject.toml           # Project metadata, dependencies, build config (using hatch)
├── src/
│   └── mimearchivefs/
│       ├── __init__.py      # Exports MimeArchiveFileSystem, core functions
│       ├── cli.py           # Optional CLI interface (using fire/rich)
│       ├── core.py          # Parsing & writing logic for the .mht format
│       ├── exceptions.py    # Custom exceptions
│       ├── filesystem.py    # fsspec implementation (MimeArchiveFileSystem, MimeArchiveFile)
│       ├── archive.py       # ZipFile-like API implementation
│       └── utils.py         # Helper functions (path handling, encoding etc.)
└── tests/
    ├── conftest.py          # Pytest fixtures
    ├── fixtures/            # Sample .mht files for testing
    │   ├── empty.mht
    │   ├── simple.mht
    │   └── binary.mht
    ├── test_cli.py          # Tests for the CLI
    ├── test_core.py         # Unit tests for parsing/writing
    ├── test_filesystem.py   # Integration tests using fsspec's test suite
    ├── test_archive.py      # Tests for the ZipFile-like API
    └── test_utils.py        # Tests for utility functions
```

### 2.5. Key Classes & Functions

-   **`src/mimearchivefs/filesystem.py`:**
    -   `MimeArchiveFileSystem(fsspec.spec.AbstractFileSystem)`
        -   `__init__(self, path_to_mht, mode='r', **storage_options)`: Loads/parses the MHT file on init.
        -   `_load_archive(self)`: Internal method to parse the MHT.
        -   `ls`, `info`, `exists`, `cat_file`, `open`, etc. (Standard fsspec methods)
        -   (Write methods): `pipe_file`, `put_file`, `rm_file`, `save()` etc.
    -   `MimeArchiveFile(fsspec.spec.AbstractBufferedFile)`: File-like object returned by `open()`. Handles reading (and potentially writing) content, including decoding Base64.
-   **`src/mimearchivefs/core.py`:**
    -   `parse_mht(file_obj)`: Takes a file-like object, parses the MIME structure using `email.parser`, extracts files, decodes content, and returns a structured representation (e.g., `dict[str, bytes | str]`).
    -   `write_mht(file_obj, file_data: dict)`: Takes a structured representation, constructs the MIME message using `email.message` / `email.mime`, encodes binary files, and writes to the file-like object.
    -   Helper functions for identifying file boundaries, extracting paths, handling encodings.
-   **`src/mimearchivefs/archive.py`:**
    -   `MimeArchive`: Main class similar to `ZipFile`.
    -   `MimeArchiveInfo`: Class similar to `ZipInfo` for file metadata.
-   **`src/mimearchivefs/exceptions.py`:**
    -   `MimeArchiveFormatError(Exception)`: For parsing errors.
    -   `FileNotFoundInArchiveError(FileNotFoundError)`: Specific file not found.
-   **`src/mimearchivefs/cli.py`:**
    -   Command-line interface for working with MimeArchive files.
    -   Functions to mount the archive as a filesystem.

### 2.6. Dependencies

-   **Core:** `fsspec`
-   **Standard Library:** `email`, `base64`, `mimetypes`, `io`, `os`
-   **Development:** `pytest`, `pytest-cov`, `ruff`, `mypy`, `hatch` (or `uv`), `pre-commit`
-   **Optional CLI:** `python-fire`, `rich`
-   **Optional Mounting:** `pyfuse3` or `fusepy`
-   **Optional Docs:** `sphinx` or `mkdocs`

### 2.7. Development & Testing

-   **Environment:** Use `hatch` or `uv` for virtual environment and dependency management.
-   **Linting/Formatting:** `ruff` (configured in `pyproject.toml`), `mypy` for type checking.
-   **Testing:** `pytest`. Use `fsspec.tests.abstract.AbstractFileSystemTests` for comprehensive filesystem interface testing. Add specific unit tests for `core.py` logic.
-   **CI:** GitHub Actions to run tests, linters on pushes/PRs.

### 2.8. Documentation

-   **README:** High-level overview, installation, quick start.
-   **Usage Guide:** Detailed examples of reading and writing archives.
-   **API Reference:** Auto-generated from docstrings (using Sphinx autodoc or similar).
-   **Format Spec:** Clear description of the `--- FILE: ---` marker and expected MIME structure.

