# this_file: tests/test_utils.py

"""Tests for utility functions."""

from mimearchivefs.utils import get_filename, get_parent_dir, normalize_path


def test_normalize_path():
    """Test path normalization."""
    assert normalize_path("/a/b/c/") == "a/b/c"
    assert normalize_path("a/b/c") == "a/b/c"
    assert normalize_path("/") == ""
    assert normalize_path("") == ""
    assert normalize_path("a") == "a"


def test_get_parent_dir():
    """Test getting the parent directory."""
    assert get_parent_dir("a/b/c") == "a/b"
    assert get_parent_dir("/a/b/c/") == "a/b"
    assert get_parent_dir("a") == ""
    assert get_parent_dir("/a") == ""
    assert get_parent_dir("") == ""  # os.path.dirname behaviour


def test_get_filename():
    """Test getting the filename."""
    assert get_filename("a/b/c") == "c"
    assert get_filename("/a/b/c/") == "c"
    assert get_filename("a") == "a"
    assert get_filename("/a") == "a"
    assert get_filename("") == ""  # os.path.basename behaviour
