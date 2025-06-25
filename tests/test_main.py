import pytest

from my_package.main import hello, add


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("World", "Hello, World!"),
        ("Jules", "Hello, Jules!"),
        ("", "Hello, !"),
        (" ", "Hello,  !"),
        ("123", "Hello, 123!"), # Test with a string number
        # Note: hello() takes `name: str`. Non-str inputs might be relevant
        # if type checking isn't strictly enforced at runtime by other means,
        # but f-strings will call str() on them.
        # For example, hello(123) would become "Hello, 123!"
    ],
)
def test_hello(name, expected):
    """Test the hello function with various inputs."""
    assert hello(name) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected_sum"),
    [
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
        (100, 200, 300),
        (-10, -20, -30),
    ],
)
def test_add(a, b, expected_sum):
    """Test the add function."""
    assert add(a, b) == expected_sum


def test_add_type_error():
    """Test that add raises TypeError for invalid input types."""
    with pytest.raises(TypeError):
        add("a", "b")  # type: ignore
    with pytest.raises(TypeError):
        add(1, "b")  # type: ignore
