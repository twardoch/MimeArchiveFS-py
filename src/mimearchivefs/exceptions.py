#!/usr/bin/env python3
# this_file: src/mimearchivefs/exceptions.py

"""Exceptions for MimeArchiveFS."""


class MimeArchiveFormatError(Exception):
    """Raised when there is an error parsing a MimeArchive file."""

    pass


class FileNotFoundInArchiveError(FileNotFoundError):
    """Raised when a file is not found in a MimeArchive."""

    pass


class InvalidPathError(ValueError):
    """Raised when a path is invalid."""

    pass


class ArchiveWriteError(IOError):
    """Raised when there is an error writing to a MimeArchive file."""

    pass
