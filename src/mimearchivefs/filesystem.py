#!/usr/bin/env python3
# this_file: src/mimearchivefs/filesystem.py

"""
Filesystem implementation for MimeArchiveFS.
"""

import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fsspec.spec import AbstractBufferedFile, AbstractFileSystem

import mimearchivefs.core as core
import mimearchivefs.utils as utils

# Forward reference for type checking
if TYPE_CHECKING:
    type MimeArchiveFileSystemType = "MimeArchiveFileSystem"


class MimeArchiveFile(AbstractBufferedFile):
    """File-like interface to files within a MimeArchive."""

    def __init__(
        self,
        fs: "MimeArchiveFileSystem",
        path: str,
        mode: str = "rb",
        **kwargs: Any,
    ) -> None:
        """
        Initialize file object.

        Args:
            fs: Parent filesystem
            path: Path to the file within the archive
            mode: File mode (r, rb, w, wb)
            **kwargs: Additional arguments to pass to AbstractBufferedFile
        """
        # Get file data from the parent filesystem
        self.path = utils.normalize_path(path)
        self.fs = fs

        # Set up initial state
        self.size = self.fs.info(self.path)["size"]

        # Initialize with AbstractBufferedFile
        super().__init__(fs=fs, path=path, mode=mode, **kwargs)

    def _fetch_range(self, start: int, end: int) -> bytes:
        """
        Fetch a range of bytes from the file.

        Args:
            start: Start position
            end: End position

        Returns:
            Bytes from the requested range
        """
        # Get data from the parent filesystem
        data = self.fs.content.get(self.path, b"")

        # Cut to the requested range
        return data[start:end]


class MimeArchiveFileSystem(AbstractFileSystem):
    """Filesystem interface for MimeArchive files."""

    protocol = "mimearchive"

    def __init__(
        self,
        path_to_mht: str | None = None,
        mode: str = "r",
        **storage_options: Any,
    ) -> None:
        """
        Initialize MimeArchiveFileSystem.

        Args:
            path_to_mht: Path to the MHT file
            mode: Access mode (r, w, a)
            **storage_options: Additional storage options
        """
        super().__init__(**storage_options)

        # Set up initial state
        self.path_to_mht = path_to_mht
        self.mode = mode
        self.content: dict[str, bytes] = {}
        self.loaded = False

        # If path is provided, load the archive
        if path_to_mht is not None:
            self._load_archive()

    def _load_archive(self) -> None:
        """Load and parse the MHT archive."""
        # Only load once
        if self.loaded:
            return

        # Check if file exists
        if self.path_to_mht is None:
            if self.mode != "w":
                raise ValueError("path_to_mht must be provided when not in write mode")
            # In write mode, start with an empty archive
            self.content = {}
        elif not Path(self.path_to_mht).exists():
            if self.mode != "w":
                # File does not exist and we're not in write mode
                raise FileNotFoundError(f"File not found: {self.path_to_mht}")
            # In write mode, start with an empty archive
            self.content = {}
        else:
            # Parse MHT file
            self.content = core.parse_mht(self.path_to_mht)

        self.loaded = True

    def _get_dirs(self) -> list[str]:
        """
        Get a list of all directories in the archive.

        Returns:
            List of directory paths
        """
        # Extract all parent directories from file paths
        dirs = set()
        for path in self.content.keys():
            parent = utils.get_parent_dir(path)
            while parent:
                dirs.add(parent)
                parent = utils.get_parent_dir(parent)

        dirs.add("")  # Add root directory
        return sorted(list(dirs))

    def ls(self, path: str = "", detail: bool = False, **kwargs: Any) -> list[str | dict[str, Any]]:
        """
        List directory contents.

        Args:
            path: Directory path
            detail: Whether to return detailed information
            **kwargs: Additional arguments

        Returns:
            List of file paths or file info dictionaries
        """
        # Ensure archive is loaded
        if not self.loaded:
            self._load_archive()

        path = utils.normalize_path(path)

        # Find all files in this directory
        all_dirs = self._get_dirs()

        # Start with all directories
        contents = []

        # Add directories that are direct children of this path
        if path == "":
            # Get all top-level directories
            for d in all_dirs:
                if "/" not in d and d != "":
                    contents.append(d)
        else:
            # Get direct child directories
            path_prefix = f"{path}/"
            for d in all_dirs:
                if d.startswith(path_prefix) and d != path:
                    # Check if it's a direct child (no additional slashes)
                    rel_path = d[len(path_prefix) :]
                    if "/" not in rel_path:
                        contents.append(d)

        # Add files that are direct children of this path
        for filepath in self.content.keys():
            if path == "":
                # Files in the root directory
                if "/" not in filepath:
                    contents.append(filepath)
            elif filepath.startswith(f"{path}/"):
                # Files in a subdirectory
                rel_path = filepath[len(path) + 1 :]
                if "/" not in rel_path:
                    contents.append(filepath)

        # Format results
        if detail:
            return [self.info(f) for f in contents]
        else:
            # Return just the file/directory names, not full paths
            return [utils.get_filename(f) for f in contents]

    def info(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """
        Get file or directory information.

        Args:
            path: Path to file or directory
            **kwargs: Additional arguments

        Returns:
            File information dictionary
        """
        # Ensure archive is loaded
        if not self.loaded:
            self._load_archive()

        path = utils.normalize_path(path)

        # Check if it's a file
        if path in self.content:
            # It's a file
            return {
                "name": path,
                "size": len(self.content[path]),
                "type": "file",
                "mtime": time.time(),  # Current time as we don't track modification times
            }

        # Check if it's a directory
        all_dirs = self._get_dirs()
        if path in all_dirs or path == "":
            # It's a directory
            return {
                "name": path,
                "size": 0,
                "type": "directory",
                "mtime": time.time(),
            }

        # Not found
        raise FileNotFoundError(f"File or directory not found: {path}")

    def exists(self, path: str, **kwargs: Any) -> bool:
        """
        Check if a file or directory exists.

        Args:
            path: Path to check
            **kwargs: Additional arguments

        Returns:
            True if file or directory exists, False otherwise
        """
        # Ensure archive is loaded
        if not self.loaded:
            self._load_archive()

        path = utils.normalize_path(path)

        # Check if it's a file
        if path in self.content:
            return True

        # Check if it's a directory
        all_dirs = self._get_dirs()
        if path in all_dirs or path == "":
            return True

        return False

    def cat_file(
        self, path: str, start: int | None = None, end: int | None = None, **kwargs: Any
    ) -> bytes:
        """
        Return contents of a file as bytes.

        Args:
            path: Path to file
            start: Start position for slicing
            end: End position for slicing
            **kwargs: Additional arguments

        Returns:
            File contents as bytes
        """
        # Ensure archive is loaded
        if not self.loaded:
            self._load_archive()

        path = utils.normalize_path(path)

        if path not in self.content:
            raise FileNotFoundError(f"File not found: {path}")

        data = self.content[path]

        # Handle slicing
        if start is not None or end is not None:
            start = start or 0
            end = end or len(data)
            return data[start:end]

        return data

    def open(
        self,
        path: str,
        mode: str = "rb",
        block_size: int | None = None,
        autocommit: bool = True,
        **kwargs: Any,
    ) -> MimeArchiveFile:
        """
        Open a file.

        Args:
            path: Path to file
            mode: File mode (r, rb, w, wb)
            block_size: Block size for buffered I/O
            autocommit: Whether to save changes automatically
            **kwargs: Additional arguments

        Returns:
            File-like object
        """
        # Ensure archive is loaded
        if not self.loaded:
            self._load_archive()

        path = utils.normalize_path(path)

        if "r" in mode:
            if path not in self.content:
                raise FileNotFoundError(f"File not found: {path}")

        return MimeArchiveFile(self, path, mode=mode, **kwargs)

    def _save(self, target: str | None = None) -> None:
        """
        Save the archive to a file.

        Args:
            target: Target file path (default: self.path_to_mht)
        """
        if target is None:
            target = self.path_to_mht

        if target is None:
            raise ValueError("No target file specified")

        # Convert bytes to strings where possible for readability
        file_data: dict[str, str | bytes] = {}
        for path, content in self.content.items():
            try:
                # Try to decode as UTF-8
                file_data[path] = content.decode("utf-8")
            except UnicodeDecodeError:
                # Keep as bytes if not UTF-8
                file_data[path] = content

        # Write the archive
        core.write_mht(target, file_data)

    def rm_file(self, path: str, **kwargs: Any) -> None:
        """
        Remove a file.

        Args:
            path: Path to file
            **kwargs: Additional arguments
        """
        # Ensure archive is loaded
        if not self.loaded:
            self._load_archive()

        path = utils.normalize_path(path)

        if path not in self.content:
            raise FileNotFoundError(f"File not found: {path}")

        del self.content[path]

        # Save changes if auto_save is enabled
        if kwargs.get("auto_save", False):
            self._save()

    def rmdir(self, path: str, **kwargs: Any) -> None:
        """
        Remove a directory.

        Args:
            path: Path to directory
            **kwargs: Additional arguments
        """
        # Ensure archive is loaded
        if not self.loaded:
            self._load_archive()

        path = utils.normalize_path(path)

        # Check if directory exists
        all_dirs = self._get_dirs()
        if path not in all_dirs and path != "":
            raise FileNotFoundError(f"Directory not found: {path}")

        # Find all files in this directory
        path_prefix = f"{path}/"
        files_to_remove = [f for f in self.content.keys() if f.startswith(path_prefix)]

        # Remove all files
        for f in files_to_remove:
            del self.content[f]

        # Save changes if auto_save is enabled
        if kwargs.get("auto_save", False):
            self._save()

    def mkdir(self, path: str, create_parents: bool = True, **kwargs: Any) -> None:
        """
        Create a directory.

        Args:
            path: Path to directory
            create_parents: Whether to create parent directories
            **kwargs: Additional arguments
        """
        # Directories don't need to be explicitly created in this filesystem
        # They exist implicitly when files are added
        pass

    def pipe_file(
        self, path: str, value: str | bytes, encoding: str = "utf-8", **kwargs: Any
    ) -> None:
        """
        Write to a file.

        Args:
            path: Path to file
            value: Data to write
            encoding: Encoding for string data
            **kwargs: Additional arguments
        """
        # Ensure archive is loaded
        if not self.loaded:
            self._load_archive()

        path = utils.normalize_path(path)

        # Convert to bytes if needed
        if isinstance(value, str):
            value = value.encode(encoding)

        # Add or update file
        self.content[path] = value

        # Save changes if auto_save is enabled
        if kwargs.get("auto_save", False):
            self._save()

    def save(self, target: str | None = None) -> None:
        """
        Save the archive to a file.

        Args:
            target: Target file path (default: self.path_to_mht)
        """
        self._save(target)
