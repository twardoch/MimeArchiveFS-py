#!/usr/bin/env python3
# this_file: src/mimearchivefs/__init__.py

"""
MimeArchiveFS - A virtual filesystem for MHTML-compatible single-file archives.
"""

# Import main classes for convenience
from .archive import MimeArchive, MimeArchiveInfo
from .core import parse_mht, write_mht
from .filesystem import MimeArchiveFileSystem
from .operations import (
    create_operation,
    extract_operation,
    mount_operation,
    version_operation,
)

__version__ = "0.1.0"
__all__ = [
    "MimeArchiveFileSystem",
    "parse_mht",
    "write_mht",
    "MimeArchive",
    "MimeArchiveInfo",
    "create_operation",
    "extract_operation",
    "mount_operation",
    "version_operation",
]
