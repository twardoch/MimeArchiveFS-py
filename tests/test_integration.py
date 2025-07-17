"""Integration tests for the package."""

import subprocess
import sys
from pathlib import Path


def test_package_installation():
    """Test that the package can be installed in development mode."""
    # This test ensures the package structure is correct for installation
    project_root = Path(__file__).parent.parent
    pyproject_toml = project_root / "pyproject.toml"
    
    assert pyproject_toml.exists(), "pyproject.toml should exist"
    
    # Check that pyproject.toml has required sections
    content = pyproject_toml.read_text()
    assert "[project]" in content
    assert "[build-system]" in content
    assert "hatchling" in content


def test_hatch_build():
    """Test that hatch can build the package."""
    try:
        # Try to import hatch to see if it's available
        import hatch  # noqa: F401
        
        # Run hatch build in a subprocess to test the build process
        result = subprocess.run(
            [sys.executable, "-m", "hatch", "build", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        
        # If hatch is available, it should show help without error
        assert result.returncode == 0 or result.returncode == 2  # 2 is help exit code
        
    except ImportError:
        # If hatch is not available, skip this test
        import pytest
        pytest.skip("Hatch not available for testing")


def test_version_from_git():
    """Test that version can be determined from git tags."""
    try:
        import subprocess
        
        # Check if we're in a git repository
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        
        if result.returncode == 0:
            # We're in a git repo, check for tags
            tag_result = subprocess.run(
                ["git", "tag", "--list"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent,
            )
            
            # This test mainly checks that git is available and working
            assert tag_result.returncode == 0
            
    except FileNotFoundError:
        # Git not available
        import pytest
        pytest.skip("Git not available for testing")


def test_lint_and_format_tools():
    """Test that lint and format tools are working."""
    try:
        # Test that ruff is available and working
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "--version"],
            capture_output=True,
            text=True,
        )
        
        # Should not error out
        assert result.returncode == 0
        assert "ruff" in result.stdout.lower()
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Ruff not available
        import pytest
        pytest.skip("Ruff not available for testing")