#!/usr/bin/env python3
# this_file: tests/conftest.py

"""Test fixtures for MimeArchiveFS."""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add the src directory to the Python path for testing
src_dir = str(Path(__file__).parents[2] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


@pytest.fixture
def sample_mht_path():
    """Create a temporary MHT file for testing."""
    from mimearchivefs.core import write_mht

    # Create test data
    test_data = {
        "file1.txt": "This is file 1",
        "dir1/file2.txt": "This is file 2",
        "dir1/dir2/file3.txt": "This is file 3",
    }

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mht", delete=False) as temp_file:
        temp_path = temp_file.name

    # Write test data to the file
    write_mht(temp_path, test_data)

    yield temp_path

    # Clean up
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def binary_mht_path():
    """Create a temporary MHT file with binary data for testing."""
    from mimearchivefs.core import write_mht

    # Create test data with binary content
    binary_data = bytes(range(256))  # All byte values from 0 to 255
    test_data = {"binary.bin": binary_data, "text.txt": "This is a text file"}

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mht", delete=False) as temp_file:
        temp_path = temp_file.name

    # Write test data to the file
    write_mht(temp_path, test_data)

    yield temp_path

    # Clean up
    if os.path.exists(temp_path):
        os.unlink(temp_path)
