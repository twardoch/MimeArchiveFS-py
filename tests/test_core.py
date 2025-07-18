#!/usr/bin/env python3
# this_file: tests/test_core.py

"""Tests for core module."""

import io
import os
import tempfile

from mimearchivefs.core import parse_mht, write_mht


def test_write_and_parse_mht():
    """Test writing and parsing MHT files."""
    # Test data
    test_data = {
        "file1.txt": "This is a test file",
        "dir1/file2.txt": "Another test file in a directory",
        "dir1/dir2/file3.txt": "Nested file",
    }

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mht", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Write test data to file
        write_mht(temp_path, test_data)

        # Read back the data
        parsed_data = parse_mht(temp_path)

        # Check that all files are present
        assert set(parsed_data.keys()) == set(test_data.keys())

        # Check file contents
        for path, content in test_data.items():
            assert parsed_data[path].decode("utf-8") == content
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_parse_mht_file_like():
    """Test parsing MHT from file-like object."""
    # Test data
    test_data = {
        "file1.txt": "This is a test file",
    }

    # Write to bytes buffer
    buffer = io.BytesIO()
    write_mht(buffer, test_data)

    # Reset buffer position
    buffer.seek(0)

    # Parse from buffer
    parsed_data = parse_mht(buffer)

    # Check data
    assert set(parsed_data.keys()) == set(test_data.keys())
    assert parsed_data["file1.txt"].decode("utf-8") == test_data["file1.txt"]


def test_binary_content():
    """Test handling binary content."""
    # Create binary data
    binary_data = bytes([0, 1, 2, 3, 255, 254, 253, 252])

    # Test data with binary
    test_data = {"binary.bin": binary_data, "text.txt": "Text file"}

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mht", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Write test data to file
        write_mht(temp_path, test_data)

        # Read back the data
        parsed_data = parse_mht(temp_path)

        # Check binary data
        assert parsed_data["binary.bin"] == binary_data
        assert parsed_data["text.txt"].decode("utf-8") == test_data["text.txt"]
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)
