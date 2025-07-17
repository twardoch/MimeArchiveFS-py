# GitHub Workflows Setup

Due to GitHub App permission restrictions, the GitHub Actions workflow files need to be manually updated.

## Issue

The GitHub App cannot modify workflow files (`.github/workflows/*.yml`) without `workflows` permission. The existing `main.yml` needs to be enhanced, and new workflow files need to be added.

## Required Changes

### 1. Update `.github/workflows/main.yml`

Replace the existing content with:

```yaml
name: CI/CD Pipeline

on: 
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  test:
    name: Test on ${{ matrix.os }} with Python ${{ matrix.python-version }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
      fail-fast: false

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies (Unix)
      if: runner.os != 'Windows'
      run: |
        python -m pip install --upgrade pip
        pip install pipx
        pipx install hatch
        pipx install uv
        pipx ensurepath
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies (Windows)
      if: runner.os == 'Windows'
      run: |
        python -m pip install --upgrade pip
        pip install pipx
        pipx install hatch
        pipx install uv
        pipx ensurepath
        echo "$env:USERPROFILE\.local\bin" | Out-File -FilePath $env:GITHUB_PATH -Encoding utf8 -Append

    - name: Configure Hatch to use uv
      run: hatch config set dirs.env.virtual.uv $(command -v uv)

    - name: Run Linting and Type Checking
      if: matrix.python-version == '3.10' && matrix.os == 'ubuntu-latest'
      run: hatch run lint:check

    - name: Run Tests
      run: hatch run default:test

    - name: Upload coverage reports
      if: matrix.python-version == '3.10' && matrix.os == 'ubuntu-latest'
      uses: codecov/codecov-action@v3
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        files: ./coverage.xml
        fail_ci_if_error: false
        verbose: true

  build:
    name: Build Package
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pipx
        pipx install hatch
        pipx install uv
        pipx ensurepath
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Configure Hatch to use uv
      run: hatch config set dirs.env.virtual.uv $(command -v uv)

    - name: Build package
      run: hatch build

    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist-files
        path: dist/
        retention-days: 30
```

### 2. Add `.github/workflows/release.yml`

Create this new file:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  test:
    name: Test on ${{ matrix.os }} with Python ${{ matrix.python-version }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
      fail-fast: false

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies (Unix)
      if: runner.os != 'Windows'
      run: |
        python -m pip install --upgrade pip
        pip install pipx
        pipx install hatch
        pipx install uv
        pipx ensurepath
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies (Windows)
      if: runner.os == 'Windows'
      run: |
        python -m pip install --upgrade pip
        pip install pipx
        pipx install hatch
        pipx install uv
        pipx ensurepath
        echo "$env:USERPROFILE\.local\bin" | Out-File -FilePath $env:GITHUB_PATH -Encoding utf8 -Append

    - name: Configure Hatch to use uv
      run: hatch config set dirs.env.virtual.uv $(command -v uv)

    - name: Run Linting and Type Checking
      if: matrix.python-version == '3.10' && matrix.os == 'ubuntu-latest'
      run: hatch run lint:check

    - name: Run Tests
      run: hatch run default:test

  build:
    name: Build Package
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pipx
        pipx install hatch
        pipx install uv
        pipx ensurepath
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Configure Hatch to use uv
      run: hatch config set dirs.env.virtual.uv $(command -v uv)

    - name: Build package
      run: hatch build

    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist-files
        path: dist/
        retention-days: 90

  create-release:
    name: Create GitHub Release
    runs-on: ubuntu-latest
    needs: build
    permissions:
      contents: write
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist-files
        path: dist/

    - name: Get version from tag
      id: get_version
      run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT

    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        tag_name: ${{ steps.get_version.outputs.VERSION }}
        name: Release ${{ steps.get_version.outputs.VERSION }}
        body: |
          # Release ${{ steps.get_version.outputs.VERSION }}
          
          ## Installation
          
          ```bash
          pip install my-package==${{ steps.get_version.outputs.VERSION }}
          ```
          
        files: |
          dist/*
        draft: false
        prerelease: false

  publish-pypi:
    name: Publish to PyPI
    runs-on: ubuntu-latest
    needs: build
    if: startsWith(github.ref, 'refs/tags/')
    environment: release
    permissions:
      id-token: write
    
    steps:
    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist-files
        path: dist/

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        verify-metadata: false
```

### 3. Add `.github/workflows/binaries.yml`

Create this new file for binary builds:

```yaml
name: Build Binaries

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build-binaries:
    name: Build ${{ matrix.target }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - target: linux-x86_64
            os: ubuntu-latest
            python-version: '3.10'
          - target: macos-x86_64
            os: macos-latest
            python-version: '3.10'
          - target: windows-x86_64
            os: windows-latest
            python-version: '3.10'

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies (Unix)
      if: runner.os != 'Windows'
      run: |
        python -m pip install --upgrade pip
        pip install pipx
        pipx install hatch
        pipx install uv
        pipx install pyinstaller
        pipx ensurepath
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies (Windows)
      if: runner.os == 'Windows'
      run: |
        python -m pip install --upgrade pip
        pip install pipx
        pipx install hatch
        pipx install uv
        pipx install pyinstaller
        pipx ensurepath
        echo "$env:USERPROFILE\.local\bin" | Out-File -FilePath $env:GITHUB_PATH -Encoding utf8 -Append

    - name: Configure Hatch to use uv
      run: hatch config set dirs.env.virtual.uv $(command -v uv)

    - name: Install package in development mode
      run: hatch run pip install -e .

    - name: Build binary (Unix)
      if: runner.os != 'Windows'
      run: |
        hatch run pyinstaller --onefile --name my-package-${{ matrix.target }} cli/main.py
        chmod +x dist/my-package-${{ matrix.target }}

    - name: Build binary (Windows)
      if: runner.os == 'Windows'
      run: |
        hatch run pyinstaller --onefile --name my-package-${{ matrix.target }}.exe cli/main.py

    - name: Test binary (Unix)
      if: runner.os != 'Windows'
      run: |
        ./dist/my-package-${{ matrix.target }} hello "World"
        ./dist/my-package-${{ matrix.target }} add 2 3

    - name: Test binary (Windows)
      if: runner.os == 'Windows'
      run: |
        ./dist/my-package-${{ matrix.target }}.exe hello "World"
        ./dist/my-package-${{ matrix.target }}.exe add 2 3

    - name: Upload binary artifacts
      uses: actions/upload-artifact@v3
      with:
        name: binaries-${{ matrix.target }}
        path: dist/my-package-*
        retention-days: 90

  create-binary-release:
    name: Create Binary Release
    runs-on: ubuntu-latest
    needs: build-binaries
    if: startsWith(github.ref, 'refs/tags/')
    permissions:
      contents: write
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Download all artifacts
      uses: actions/download-artifact@v3
      with:
        path: artifacts/

    - name: Organize binaries
      run: |
        mkdir -p binaries
        find artifacts/ -name "my-package-*" -type f -exec cp {} binaries/ \;
        ls -la binaries/

    - name: Get version from tag
      id: get_version
      run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT

    - name: Create checksums
      run: |
        cd binaries
        sha256sum * > checksums.txt
        cat checksums.txt

    - name: Update release with binaries
      uses: softprops/action-gh-release@v1
      with:
        tag_name: ${{ steps.get_version.outputs.VERSION }}
        files: |
          binaries/*
        append_body: true
        body: |
          
          ## Binary Downloads
          
          - **Linux (x86_64)**: `my-package-linux-x86_64`
          - **macOS (x86_64)**: `my-package-macos-x86_64`
          - **Windows (x86_64)**: `my-package-windows-x86_64.exe`
          
          ### Usage
          
          ```bash
          # Unix
          chmod +x my-package-*
          ./my-package-* hello "World"
          
          # Windows
          my-package-*.exe hello "World"
          ```
```

## Setup Instructions

1. **Update existing workflow**: Replace `.github/workflows/main.yml` with the enhanced version above
2. **Add new workflows**: Create the `release.yml` and `binaries.yml` files
3. **Update package references**: Replace `my-package` with your actual package name
4. **Test**: Push changes and create a test tag to verify everything works

## Benefits

- **Multiplatform testing**: All Python versions across Linux, macOS, Windows
- **Automated releases**: Create releases by pushing git tags
- **Binary distribution**: Standalone executables for easy installation
- **PyPI publishing**: Automatic package publishing (configure PyPI trusted publishing)

## Notes

- The workflows are configured for Python package structure with `src/` layout
- Binary builds require the `cli/main.py` script to be present
- PyPI publishing uses trusted publishing (no API tokens needed)
- All package names should be updated to match your actual package