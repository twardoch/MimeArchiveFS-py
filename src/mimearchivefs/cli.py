#!/usr/bin/env python3
# this_file: src/mimearchivefs/cli.py

"""
Command line entry point for MimeArchiveFS.
"""

import fire

from mimearchivefs.operations import (
    create_operation,
    extract_operation,
    mount_operation,
    version_operation,
)


class MimeArchiveFsCli:
    """Command-line interface for the MimeArchiveFS package."""

    def __init__(self, verbose: bool = False) -> None:
        """Initialize the CLI.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose

    def mount(self, file_path: str, mount_point: str | None = None) -> None:
        """Mount an MHT file as a virtual filesystem.

        Args:
            file_path: Path to the MHT file to mount
            mount_point: Folder to mount the filesystem at (optional)
        """
        mount_operation(mht_file=file_path, mount_point=mount_point, debug=self.verbose)

    def unpack(self, file_path: str, output_dir: str = ".") -> None:
        """Unpack contents from an MHT file to a folder.

        Args:
            file_path: Path to the MHT file to unpack
            output_dir: Folder to unpack files to (default: current folder)
        """
        extract_operation(mht_file=file_path, output_dir=output_dir, debug=self.verbose)

    def pack(
        self,
        folder: str,
        output_file: str | None = None,
        with_hidden: bool = False,
        with_symlinks: bool = False,
    ) -> None:
        """Pack a folder into an MHT file.

        Args:
            folder: Path to the folder to pack
            output_file: Path to the output MHT file (optional - outputs to stdout if not provided)
            with_hidden: Include hidden files (starting with .)
            with_symlinks: Follow symbolic links when traversing directories
        """
        create_operation(
            folder=folder,
            output_file=output_file,
            debug=self.verbose,
            with_hidden=with_hidden,
            with_symlinks=with_symlinks,
        )

    def version(self) -> None:
        """Display version information."""
        version_operation()


def main() -> None:
    """Entry point for the CLI."""
    fire.Fire(MimeArchiveFsCli)


if __name__ == "__main__":
    main()
