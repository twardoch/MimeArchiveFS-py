#!/usr/bin/env python3
# this_file: examples/mimearchivefs_cli.py
"""
Example CLI for MimeArchiveFS.

This is an example script showing how to create a CLI interface for MimeArchiveFS
using the Python Fire library. It demonstrates basic operations like packing,
unpacking, listing, adding, removing, and copying files.

Usage:
    python mimearchivefs_cli.py pack <source_dir> <archive_path>
    python mimearchivefs_cli.py unpack <archive_path> <target_dir>
    python mimearchivefs_cli.py list <archive_path>
    python mimearchivefs_cli.py add <archive_path> <file_path> [<archive_file_path>]
    python mimearchivefs_cli.py remove <archive_path> <file_path>
    python mimearchivefs_cli.py copy <source_archive> <target_archive> <file_path>
"""

import os
import sys

try:
    import fire
    from rich import print
    from rich.console import Console
    from rich.table import Table
except ImportError:
    print("This example requires additional dependencies. Install with:")
    print("pip install fire rich")
    sys.exit(1)

# Add the module in development to path if needed
if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")):
    print("Warning: src directory not found. Make sure you're running from the project root.")
else:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

try:
    from mimearchivefs import MimeArchiveFileSystem
    from mimearchivefs.archive import MimeArchive
except ImportError:
    print("Error: MimeArchiveFS module not found.")
    print("Make sure you're running from the project root or the package is installed.")
    sys.exit(1)

console = Console()


class MimeArchiveCLI:
    """CLI for working with MimeArchive (.mht) files."""

    def pack(self, source_dir: str, archive_path: str) -> None:
        """
        Pack a directory into an MHT archive.

        Args:
            source_dir: Source directory to pack
            archive_path: Path to the output archive
        """
        if not os.path.isdir(source_dir):
            print(f"[red]Error: Source directory '{source_dir}' not found.[/red]")
            return

        try:
            # Create a new archive in write mode
            fs = MimeArchiveFileSystem(archive_path, mode="w")

            # Track the number of files added
            file_count = 0
            total_size = 0

            # Recursively add all files from the source directory
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate the relative path for the archive
                    rel_path = os.path.relpath(file_path, source_dir)

                    # Read the file content
                    with open(file_path, "rb") as f:
                        content = f.read()

                    # Add to the archive
                    fs.pipe_file(rel_path, content)

                    # Update counters
                    file_count += 1
                    total_size += len(content)

                    # Show progress
                    print(f"Adding: {rel_path} ({len(content)} bytes)")

            # Save the archive
            fs.save()
            print(
                f"[green]Successfully packed {file_count} files ({total_size} bytes) to {archive_path}[/green]"
            )
        except Exception as e:
            print(f"[red]Error packing directory: {str(e)}[/red]")

    def unpack(self, archive_path: str, target_dir: str) -> None:
        """
        Unpack an MHT archive to a directory.

        Args:
            archive_path: Path to the archive
            target_dir: Target directory for extracted files
        """
        if not os.path.isfile(archive_path):
            print(f"[red]Error: Archive file '{archive_path}' not found.[/red]")
            return

        try:
            # Create target directory if it doesn't exist
            os.makedirs(target_dir, exist_ok=True)

            # Using MimeArchive (ZipFile-like API) for simplicity
            with MimeArchive(archive_path) as archive:
                print(f"Extracting archive to {target_dir}...")
                archive.extractall(target_dir)

                # Count extracted files
                file_count = len(archive.namelist())
                print(f"[green]Successfully extracted {file_count} files to {target_dir}[/green]")
        except Exception as e:
            print(f"[red]Error unpacking archive: {str(e)}[/red]")

    def list(self, archive_path: str) -> None:
        """
        List contents of an MHT archive.

        Args:
            archive_path: Path to the archive
        """
        if not os.path.isfile(archive_path):
            print(f"[red]Error: Archive file '{archive_path}' not found.[/red]")
            return

        try:
            # Open the archive
            fs = MimeArchiveFileSystem(archive_path)

            # Collect all files recursively
            all_files: list[tuple[str, int]] = []

            def list_recursive(path: str = "") -> None:
                if not path:
                    items = fs.ls()
                else:
                    items = fs.ls(path)

                for item in items:
                    item_str = str(item)
                    full_path = f"{path}/{item_str}" if path else item_str

                    if fs.info(full_path)["type"] == "directory":
                        list_recursive(full_path)
                    else:
                        info = fs.info(full_path)
                        all_files.append((full_path, info["size"]))

            # Get all files
            list_recursive()

            # Display files in a table
            table = Table(title=f"Contents of {archive_path}")
            table.add_column("Path", style="cyan")
            table.add_column("Size (bytes)", justify="right", style="green")

            # Add rows for each file
            for path, size in sorted(all_files):
                table.add_row(path, str(size))

            # Add summary row
            table.add_row("", "")
            table.add_row(
                f"Total: {len(all_files)} files",
                f"{sum(size for _, size in all_files)} bytes",
                style="bold",
            )

            console.print(table)
        except Exception as e:
            print(f"[red]Error listing archive: {str(e)}[/red]")

    def add(self, archive_path: str, file_path: str, archive_file_path: str | None = None) -> None:
        """
        Add a file to an MHT archive.

        Args:
            archive_path: Path to the archive
            file_path: Path to the file to add
            archive_file_path: Path within the archive (default: same as file_path basename)
        """
        if not os.path.isfile(archive_path):
            print(f"[red]Error: Archive file '{archive_path}' not found.[/red]")
            return

        if not os.path.isfile(file_path):
            print(f"[red]Error: File '{file_path}' not found.[/red]")
            return

        try:
            # Open the archive in append mode
            fs = MimeArchiveFileSystem(archive_path, mode="a")

            # If no archive path was specified, use the basename of the input file
            if archive_file_path is None:
                archive_file_path = os.path.basename(file_path)

            # Read the file content
            with open(file_path, "rb") as f:
                content = f.read()

            # Add to the archive
            fs.pipe_file(archive_file_path, content)

            # Save changes
            fs.save()
            print(
                f"[green]Added {file_path} as {archive_file_path} to {archive_path} ({len(content)} bytes)[/green]"
            )
        except Exception as e:
            print(f"[red]Error adding file to archive: {str(e)}[/red]")

    def remove(self, archive_path: str, file_path: str) -> None:
        """
        Remove a file from an MHT archive.

        Args:
            archive_path: Path to the archive
            file_path: Path to the file within the archive to remove
        """
        if not os.path.isfile(archive_path):
            print(f"[red]Error: Archive file '{archive_path}' not found.[/red]")
            return

        try:
            # Open the archive in append mode
            fs = MimeArchiveFileSystem(archive_path, mode="a")

            # Check if the file exists
            if not fs.exists(file_path):
                print(f"[red]Error: File '{file_path}' not found in the archive.[/red]")
                return

            # Get file size before removing (for reporting)
            file_size = fs.info(file_path)["size"]

            # Remove the file
            fs.rm_file(file_path)

            # Save changes
            fs.save()
            print(f"[green]Removed {file_path} ({file_size} bytes) from {archive_path}[/green]")
        except Exception as e:
            print(f"[red]Error removing file from archive: {str(e)}[/red]")

    def copy(self, source_archive: str, target_archive: str, file_path: str) -> None:
        """
        Copy a file from one MHT archive to another.

        Args:
            source_archive: Path to the source archive
            target_archive: Path to the target archive
            file_path: Path to the file within the source archive to copy
        """
        if not os.path.isfile(source_archive):
            print(f"[red]Error: Source archive '{source_archive}' not found.[/red]")
            return

        try:
            # Open both archives
            source_fs = MimeArchiveFileSystem(source_archive)

            # Check if the file exists in the source
            if not source_fs.exists(file_path):
                print(f"[red]Error: File '{file_path}' not found in the source archive.[/red]")
                return

            # Check if the target archive exists, if not create it
            target_mode = "a" if os.path.isfile(target_archive) else "w"
            target_fs = MimeArchiveFileSystem(target_archive, mode=target_mode)

            # Read content from source
            content = source_fs.cat_file(file_path)
            file_size = len(content)

            # Write to target
            target_fs.pipe_file(file_path, content)

            # Save target archive
            target_fs.save()
            print(
                f"[green]Copied {file_path} ({file_size} bytes) from {source_archive} to {target_archive}[/green]"
            )
        except Exception as e:
            print(f"[red]Error copying file between archives: {str(e)}[/red]")


if __name__ == "__main__":
    fire.Fire(MimeArchiveCLI)
