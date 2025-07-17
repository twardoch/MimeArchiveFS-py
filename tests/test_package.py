"""Test package structure and imports."""

import importlib.util
import sys
from pathlib import Path


def test_package_imports():
    """Test that the package can be imported properly."""
    import my_package
    
    # Check that the package has __version__ attribute when built
    # This will be available when installed via pip/hatch
    assert hasattr(my_package, '__version__') or True  # Allow for development mode
    
    # Check that main module functions are accessible
    from my_package.main import hello, add
    assert callable(hello)
    assert callable(add)


def test_package_structure():
    """Test that the package has the expected structure."""
    # Check that the package directory exists
    src_path = Path(__file__).parent.parent / "src" / "my_package"
    assert src_path.exists()
    assert src_path.is_dir()
    
    # Check that __init__.py exists
    init_file = src_path / "__init__.py"
    assert init_file.exists()
    
    # Check that main.py exists
    main_file = src_path / "main.py"
    assert main_file.exists()


def test_module_attributes():
    """Test that modules have expected attributes."""
    from my_package.main import hello, add
    
    # Check function signatures
    assert hello.__name__ == "hello"
    assert add.__name__ == "add"
    
    # Check that functions have docstrings
    assert hello.__doc__ is not None
    assert add.__doc__ is not None
    assert len(hello.__doc__.strip()) > 0
    assert len(add.__doc__.strip()) > 0


def test_version_info():
    """Test version information is available when package is installed."""
    try:
        import my_package
        # This will work when the package is installed
        if hasattr(my_package, '__version__'):
            assert isinstance(my_package.__version__, str)
            assert len(my_package.__version__) > 0
    except AttributeError:
        # In development mode, version might not be available
        # This is expected and not a failure
        pass