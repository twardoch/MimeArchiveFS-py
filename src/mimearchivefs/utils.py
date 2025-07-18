#!/usr/bin/env python3
# this_file: src/mimearchivefs/utils.py

"""Utility functions for the MimeArchiveFS package."""

from pathlib import Path


def normalize_path(path: str) -> str:
    """
    Normalize a path for use in the MimeArchiveFS.

    Removes leading and trailing slashes and ensures a consistent format.

    Args:
        path: Path string to normalize

    Returns:
        Normalized path string
    """
    # Remove leading and trailing slashes
    path = path.strip("/")

    # Remove any double slashes and normalize
    path = str(Path(path).as_posix())

    # Handle the special case of root
    if path == "." or path == "":
        return ""

    # Path.as_posix() already uses forward slashes, no need to replace backslashes

    return path


def get_parent_dir(path: str) -> str:
    """
    Get the parent directory of a path.

    Args:
        path: Path string

    Returns:
        Parent directory string
    """
    path = normalize_path(path)

    if not path:
        return ""

    parent = str(Path(path).parent)
    # Convert path separator to forward slash for consistency
    parent = parent.replace("\\", "/")
    return parent


def get_filename(path: str) -> str:
    """
    Get the filename from a path.

    Args:
        path: Path string

    Returns:
        Filename string
    """
    path = normalize_path(path)

    if not path:
        return ""

    filename = Path(path).name
    return filename


def is_binary_string(content: str | bytes) -> bool:
    """
    Check if string content should be treated as binary.

    Args:
        content: String or bytes content to check

    Returns:
        True if content should be treated as binary, False otherwise
    """
    if isinstance(content, bytes):
        try:
            content.decode("utf-8")
            return False
        except UnicodeDecodeError:
            return True

    # It's already a string, so it's not binary
    return False
