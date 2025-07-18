# MimeArchiveFS (`mimearchivefs`)

A virtual filesystem based on an MHTML-compatible single-file archive format (.mht).

## Overview

MimeArchiveFS-py ("MAFS") is the Python implementation of a virtual filesystem built around a mountable single-file archive format that extends MHTML and is backwards-compatible to it.

A MimeArchiveFS archive (container, MIME type `application/x-mimearchive`) is a file with the extension `.mht`, which acts as a universal container for multiple plaintext and binary files, making it ideal for packaging code repositories, markdown files, and even configuration data into a structured yet easily accessible format.

## Features

- Read and parse MHTML-compatible `.mht` files
- Access contents through a virtual filesystem interface (using `fsspec`)
- Directory listing and file status/metadata
- Read file content
- Support for both text and binary files (using Base64 encoding)

## Installation

```bash
pip install mimearchivefs
```

## Usage

```python
from mimearchivefs import MimeArchiveFileSystem

# Open a MimeArchive file as a filesystem
fs = MimeArchiveFileSystem("path/to/archive.mht")

# List files in the archive
fs.ls()

# Read a file from the archive
with fs.open("path/to/file.txt") as f:
    content = f.read()

# Check if a file exists
fs.exists("path/to/file.txt")

# Get file information
info = fs.info("path/to/file.txt")
```

## License

MIT License 