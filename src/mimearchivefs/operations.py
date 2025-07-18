#!/usr/bin/env python3
# this_file: src/mimearchivefs/operations.py

"""
Operations for the MimeArchiveFS CLI.
"""

import io
import sys
from pathlib import Path
from typing import Any, cast

from loguru import logger
from rich import print as rprint

from mimearchivefs import MimeArchiveFileSystem, write_mht


def mount_operation(mht_file: str, mount_point: str | None = None, debug: bool = False) -> None:
    """Mount an MHT file as a virtual filesystem.

    Args:
        mht_file: Path to the MHT file to mount
        mount_point: Folder to mount the filesystem at (optional)
        debug: Enable debug logging
    """
    if debug:
        logger.enable("mimearchivefs")

    fs = MimeArchiveFileSystem(mht_file)
    if mount_point:
        # Future implementation for actual FUSE mounting
        rprint("[yellow]Mount functionality not yet implemented[/yellow]")
    else:
        # Just list the files if no mount point provided
        rprint(f"[bold]Contents of {mht_file}:[/bold]")

        # Recursive function to list all files and folders
        def list_dir(path: str, indent: int = 0) -> None:
            files = fs.ls(path, detail=True)
            for file_info in files:
                # Cast to dict with proper types
                file_dict = cast(dict[str, Any], file_info)
                full_path = file_dict.get("name", "")
                name = Path(full_path).name or full_path
                file_type = file_dict.get("type", "")

                if file_type == "folder" or file_type == "directory":
                    rprint(f"{' ' * indent}[blue][bold]{name}/[/bold][/blue]")
                    list_dir(full_path, indent + 2)
                else:
                    size = file_dict.get("size", 0)
                    rprint(f"{' ' * indent}{name} ({size} bytes)")

        list_dir("")


def extract_operation(mht_file: str, output_dir: str = ".", debug: bool = False) -> None:
    """Unpack contents from an MHT file to a folder.

    Args:
        mht_file: Path to the MHT file to unpack
        output_dir: Folder to unpack files to (default: current folder)
        debug: Enable debug logging
    """
    if debug:
        logger.enable("mimearchivefs")

    try:
        fs = MimeArchiveFileSystem(mht_file)

        # Create output folder if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Get all files recursively
        def get_all_files(path: str = "") -> list[str]:
            result: list[str] = []
            files = fs.ls(path, detail=True)

            for file_info in files:
                # Cast to dict with proper types
                file_dict = cast(dict[str, Any], file_info)
                file_type = file_dict.get("type", "")
                file_name = file_dict.get("name", "")

                if file_type == "file":
                    result.append(file_name)
                elif file_type == "folder" or file_type == "directory":
                    result.extend(get_all_files(file_name))

            return result

        # Extract all files
        file_count = 0
        all_files = get_all_files()

        for file_path in all_files:
            # Create target folder
            output_path = Path(output_dir) / file_path
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Extract file content
            content = fs.cat_file(file_path)

            # Write to output file
            output_path.write_bytes(content)

            file_count += 1

        success_msg = (
            f"[green]Successfully unpacked {file_count} files from {mht_file} "
            f"to {output_dir}[/green]"
        )
        rprint(success_msg)
    except Exception as e:
        rprint(f"[red]Error unpacking {mht_file}: {e}[/red]")
        sys.exit(1)


def create_operation(
    folder: str,
    output_file: str | None = None,
    debug: bool = False,
    with_hidden: bool = False,
    with_symlinks: bool = False,
) -> None:
    """Pack a folder into an MHT file or output to stdout.

    Args:
        folder: Path to the folder to pack
        output_file: Path to the output MHT file or None for stdout output
        debug: Enable debug logging
        with_hidden: Include hidden files (starting with .)
        with_symlinks: Follow symbolic links when traversing directories
    """
    if debug:
        logger.enable("mimearchivefs")
        print(f"DEBUG: Packing folder: {folder}", file=sys.stderr)
        print(f"DEBUG: Folder exists: {Path(folder).exists()}", file=sys.stderr)
        print(f"DEBUG: Is directory: {Path(folder).is_dir()}", file=sys.stderr)
        print(f"DEBUG: Include hidden files: {with_hidden}", file=sys.stderr)
        print(f"DEBUG: Follow symlinks: {with_symlinks}", file=sys.stderr)

    try:
        # Initialize file data
        file_data: dict[str, str | bytes] = {}
        file_count = 0

        # Walk through folder and collect file data
        folder_path = Path(folder)
        if debug:
            print(f"DEBUG: Looking for files in: {folder_path.absolute()}", file=sys.stderr)

        # We need to use os.walk with followlinks=True if with_symlinks is True
        if with_symlinks:
            import os

            for root, _dirs, files in os.walk(folder_path, followlinks=True):
                for file in files:
                    path = Path(root) / file

                    # Skip hidden files unless with_hidden is True
                    if path.name.startswith(".") and not with_hidden:
                        if debug:
                            rel_path = path.relative_to(folder_path).as_posix()
                            print(
                                f"DEBUG: Skipping hidden file: {rel_path}",
                                file=sys.stderr,
                            )
                        continue

                    try:
                        # Calculate relative path
                        rel_path = path.relative_to(folder_path).as_posix()

                        # Read file content
                        content = path.read_bytes()

                        # Add to file data
                        file_data[rel_path] = content
                        file_count += 1

                        # If in debug mode, log the file being packed to stderr
                        if debug:
                            print(f"Packing ({file_count}): {rel_path}", file=sys.stderr)
                    except (PermissionError, FileNotFoundError) as e:
                        if debug:
                            print(f"WARNING: Could not read file {path}: {e}", file=sys.stderr)
        else:
            # Use Path.rglob which doesn't follow symlinks
            for path in folder_path.rglob("*"):
                if path.is_file():
                    # Calculate relative path
                    rel_path = path.relative_to(folder_path).as_posix()

                    # Skip hidden files unless with_hidden is True
                    if path.name.startswith(".") and not with_hidden:
                        if debug:
                            print(f"DEBUG: Skipping hidden file: {rel_path}", file=sys.stderr)
                        continue

                    # Read file content
                    content = path.read_bytes()

                    # Add to file data
                    file_data[rel_path] = content
                    file_count += 1

                    # If in debug mode, log the file being packed to stderr
                    if debug:
                        print(f"Packing ({file_count}): {rel_path}", file=sys.stderr)

        # If in debug mode, show total packed files
        if debug:
            print(f"Total files packed: {file_count}", file=sys.stderr)
            if file_count == 0:
                print(f"WARNING: No files were packed from {folder}", file=sys.stderr)

        # Output to stdout or file
        if output_file is None:
            # Create in-memory file-like object
            output_buffer = io.BytesIO()

            # Write data to buffer
            write_mht(output_buffer, file_data)

            # Write to stdout (binary mode)
            sys.stdout.buffer.write(output_buffer.getvalue())
        else:
            # Write directly to file
            write_mht(output_file, file_data)

    except Exception as e:
        if debug:
            print(f"Error packing archive: {e}", file=sys.stderr)
            import traceback

            traceback.print_exc(file=sys.stderr)
        sys.exit(1)


def version_operation() -> None:
    """Display version information."""
    from mimearchivefs import __version__

    rprint(f"MimeArchiveFS version [bold]{__version__}[/bold]")
