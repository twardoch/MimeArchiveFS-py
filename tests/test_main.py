import pytest

from src.main import hello, add


def test_hello():
    """Test the hello function."""
    assert hello("World") == "Hello, World!"
    assert hello("Jules") == "Hello, Jules!"


def test_add():
    """Test the add function."""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(100, 200) == 300


def test_add_type_error():
    """Test that add raises TypeError for invalid input types."""
    with pytest.raises(TypeError):
        add("a", "b")  # type: ignore
    with pytest.raises(TypeError):
        add(1, "b")  # type: ignore
