#!/usr/bin/env python3
# this_file: tests/test_filesystem.py

"""Tests for filesystem module."""

import os
import tempfile

from mimearchivefs.filesystem import MimeArchiveFileSystem


def test_filesystem_basic():
    """Test basic functionality of MimeArchiveFileSystem."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mht", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Create filesystem in write mode
        fs = MimeArchiveFileSystem(temp_path, mode="w")

        # Add some files
        fs.pipe_file("file1.txt", "Content of file 1")
        fs.pipe_file("dir1/file2.txt", "Content of file 2")
        fs.pipe_file("dir1/dir2/file3.txt", "Content of file 3")

        # Save the changes
        fs.save()

        # Reopen in read mode
        fs = MimeArchiveFileSystem(temp_path)

        # Check if files exist
        assert fs.exists("file1.txt")
        assert fs.exists("dir1/file2.txt")
        assert fs.exists("dir1/dir2/file3.txt")

        # Check directory listing
        root_ls = fs.ls()
        assert "file1.txt" in root_ls
        assert "dir1" in root_ls

        dir1_ls = fs.ls("dir1")
        assert "file2.txt" in dir1_ls
        assert "dir2" in dir1_ls

        # Check file contents
        assert fs.cat_file("file1.txt").decode("utf-8") == "Content of file 1"
        assert fs.cat_file("dir1/file2.txt").decode("utf-8") == "Content of file 2"

        # Test open method
        with fs.open("dir1/dir2/file3.txt", "r") as file:
            content = file.read()
            assert content == "Content of file 3"
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_filesystem_remove():
    """Test removing files and directories."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mht", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Create filesystem in write mode
        fs = MimeArchiveFileSystem(temp_path, mode="w")

        # Add some files
        fs.pipe_file("file1.txt", "Content of file 1")
        fs.pipe_file("dir1/file2.txt", "Content of file 2")
        fs.pipe_file("dir1/dir2/file3.txt", "Content of file 3")

        # Save the changes
        fs.save()

        # Remove a file
        fs.rm_file("file1.txt")
        assert not fs.exists("file1.txt")

        # Remove a directory
        fs.rmdir("dir1/dir2")
        assert not fs.exists("dir1/dir2/file3.txt")
        assert fs.exists("dir1/file2.txt")  # This should still exist

        # Save and reload
        fs.save()
        fs = MimeArchiveFileSystem(temp_path)

        # Check if the changes persisted
        assert not fs.exists("file1.txt")
        assert not fs.exists("dir1/dir2/file3.txt")
        assert fs.exists("dir1/file2.txt")
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_filesystem_info():
    """Test file and directory info."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mht", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Create filesystem in write mode
        fs = MimeArchiveFileSystem(temp_path, mode="w")

        # Add a file
        fs.pipe_file("file1.txt", "Content of file 1")
        fs.pipe_file("dir1/file2.txt", "Content of file 2")

        # Get file info
        file_info = fs.info("file1.txt")
        assert file_info["type"] == "file"
        assert file_info["size"] == len(b"Content of file 1")

        # Get directory info
        dir_info = fs.info("dir1")
        assert dir_info["type"] == "directory"

        # Get detailed directory listing
        dir_ls = fs.ls("", detail=True)
        assert any(item["name"] == "file1.txt" for item in dir_ls)
        assert any(item["name"] == "dir1" for item in dir_ls)
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)
