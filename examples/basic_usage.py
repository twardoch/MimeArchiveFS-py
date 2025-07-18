#!/usr/bin/env python3
# this_file: examples/basic_usage.py
"""
Basic usage examples for MimeArchiveFS.

This script demonstrates the basic operations of the MimeArchiveFS package
without using the command-line interface.

Usage:
    python basic_usage.py

The script creates a temporary directory and performs the following operations:
1. Creates a new MHT archive
2. Adds some files to it
3. Lists the contents
4. Extracts files from the archive
5. Demonstrates modifying the archive
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the module in development to path if needed
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from mimearchivefs import MimeArchiveFileSystem
    from mimearchivefs.archive import MimeArchive
except ImportError:
    print("Error: MimeArchiveFS module not found.")
    print("Make sure you're running from the project root or the package is installed.")
    sys.exit(1)


def main():
    """Run basic usage examples."""
    # Create temporary directory for examples
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Working in temporary directory: {temp_dir}")

        # Set up paths
        source_dir = os.path.join(temp_dir, "source")
        extract_dir = os.path.join(temp_dir, "extract")
        archive_path = os.path.join(temp_dir, "example.mht")

        os.makedirs(source_dir)
        os.makedirs(extract_dir)

        # Create example files
        create_example_files(source_dir)

        # Example 1: Create a new archive and add files
        create_archive(source_dir, archive_path)

        # Example 2: List archive contents
        list_archive(archive_path)

        # Example 3: Extract archive
        extract_archive(archive_path, extract_dir)

        # Example 4: Modify archive
        modify_archive(archive_path)

        print("\nAll examples completed successfully!")


def create_example_files(source_dir):
    """Create example files for testing."""
    print("\n=== Creating Example Files ===")

    # Create subdirectories
    os.makedirs(os.path.join(source_dir, "dir1", "dir2"), exist_ok=True)

    # Create text files
    files = {
        "file1.txt": "This is file 1 with some text content.",
        os.path.join("dir1", "file2.txt"): "This is file 2 in a subdirectory.",
        os.path.join("dir1", "dir2", "file3.txt"): "This is file 3 in a nested subdirectory.",
    }

    for path, content in files.items():
        full_path = os.path.join(source_dir, path)
        with open(full_path, "w") as f:
            f.write(content)
        print(f"Created: {path} ({len(content)} bytes)")

    # Create a small binary file
    binary_path = os.path.join(source_dir, "binary.dat")
    with open(binary_path, "wb") as f:
        f.write(bytes(range(256)))  # All byte values from 0 to 255
    print("Created: binary.dat (256 bytes)")


def create_archive(source_dir, archive_path):
    """Create a new archive from a source directory."""
    print("\n=== Creating New Archive ===")

    # Create filesystem in write mode
    fs = MimeArchiveFileSystem(archive_path, mode="w")

    # Add files to the archive
    for root, _, files in os.walk(source_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, source_dir)

            # Read file content
            with open(file_path, "rb") as f:
                content = f.read()

            # Add to archive
            fs.pipe_file(rel_path, content)
            print(f"Added: {rel_path} ({len(content)} bytes)")

    # Save the archive
    fs.save()
    print(f"Archive saved to: {archive_path}")


def list_archive(archive_path):
    """List contents of an archive."""
    print("\n=== Listing Archive Contents ===")

    # Open the archive
    fs = MimeArchiveFileSystem(archive_path)

    # Function to recursively list files
    def list_recursive(path: str = "", indent: int = 0):
        items = fs.ls(path)

        for item in items:
            item_str = str(item)
            full_path = f"{path}/{item_str}" if path else item_str
            info = fs.info(full_path)

            if info["type"] == "directory":
                print(f"{'  ' * indent}📁 {item_str}/")
                list_recursive(full_path, indent + 1)
            else:
                print(f"{'  ' * indent}📄 {item_str} ({info['size']} bytes)")

    # List all files and directories
    list_recursive()


def extract_archive(archive_path, extract_dir):
    """Extract archive contents."""
    print(f"\n=== Extracting Archive to {extract_dir} ===")

    # Method 1: Using MimeArchiveFileSystem
    fs = MimeArchiveFileSystem(archive_path)

    # Function to recursively extract files
    def extract_recursive(path: str = ""):
        items = fs.ls(path)

        for item in items:
            item_str = str(item)
            full_path = f"{path}/{item_str}" if path else item_str
            target_path = os.path.join(extract_dir, "method1", full_path)

            info = fs.info(full_path)
            if info["type"] == "directory":
                os.makedirs(target_path, exist_ok=True)
                extract_recursive(full_path)
            else:
                # Ensure parent directory exists
                os.makedirs(os.path.dirname(target_path), exist_ok=True)

                # Extract file
                with fs.open(full_path, "rb") as src, open(target_path, "wb") as dst:
                    content = src.read()
                    dst.write(content)
                print(f"Extracted (method1): {full_path} ({len(content)} bytes)")

    # Create extraction subdirectory
    os.makedirs(os.path.join(extract_dir, "method1"), exist_ok=True)
    extract_recursive()

    # Method 2: Using MimeArchive (ZipFile-like API)
    print("\n--- Using MimeArchive API ---")
    os.makedirs(os.path.join(extract_dir, "method2"), exist_ok=True)

    with MimeArchive(archive_path) as archive:
        archive.extractall(os.path.join(extract_dir, "method2"))

        # List extracted files
        for name in archive.namelist():
            print(f"Extracted (method2): {name}")


def modify_archive(archive_path):
    """Modify an existing archive."""
    print("\n=== Modifying Archive ===")

    # Open archive in append mode
    fs = MimeArchiveFileSystem(archive_path, mode="a")

    # Add a new file
    fs.pipe_file("new_file.txt", b"This is a new file added to the archive.")
    print("Added: new_file.txt")

    # Remove an existing file
    fs.rm_file("file1.txt")
    print("Removed: file1.txt")

    # Save changes
    fs.save()

    # Print updated contents
    print("\n--- Updated Archive Contents ---")
    all_files: list[tuple[str, int]] = []

    def collect_files(path: str = ""):
        items = fs.ls(path)

        for item in items:
            item_str = str(item)
            full_path = f"{path}/{item_str}" if path else item_str
            info = fs.info(full_path)

            if info["type"] == "directory":
                collect_files(full_path)
            else:
                all_files.append((full_path, info["size"]))

    collect_files()

    for path, size in sorted(all_files):
        print(f"📄 {path} ({size} bytes)")


if __name__ == "__main__":
    main()
