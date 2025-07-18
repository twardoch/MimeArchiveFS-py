# MimeArchiveFS Examples

This directory contains example scripts demonstrating how to use the MimeArchiveFS package.

## Shell Examples

The `mimearchivefs_cli_examples.sh` script demonstrates using MimeArchiveFS from shell scripts. It includes examples of:

- Packing a directory into an MHT archive
- Listing archive contents
- Unpacking an archive to a directory
- Adding files to an existing archive
- Removing files from an archive
- Copying files between archives

Run it with:

```bash
bash mimearchivefs_cli_examples.sh
```

## Python CLI Example

The `mimearchivefs_cli.py` script provides a command-line interface for working with MimeArchive files, using Python's Fire library. It includes commands for:

- `pack`: Pack a directory into an MHT archive
- `unpack`: Extract files from an MHT archive
- `list`: List contents of an MHT archive
- `add`: Add a file to an MHT archive
- `remove`: Remove a file from an MHT archive
- `copy`: Copy a file from one archive to another

Example usage:

```bash
# Pack a directory
python mimearchivefs_cli.py pack /path/to/source archive.mht

# List archive contents
python mimearchivefs_cli.py list archive.mht

# Unpack an archive
python mimearchivefs_cli.py unpack archive.mht /path/to/extract

# Add a file
python mimearchivefs_cli.py add archive.mht /path/to/file.txt [optional/path/in/archive.txt]

# Remove a file
python mimearchivefs_cli.py remove archive.mht path/in/archive.txt

# Copy a file between archives
python mimearchivefs_cli.py copy source.mht target.mht file/to/copy.txt
```

## Basic Python Usage

The `basic_usage.py` script demonstrates programmatic usage of the MimeArchiveFS API without a command-line interface. It shows:

- Creating a new archive
- Adding files to an archive
- Listing archive contents
- Extracting files from an archive
- Modifying an existing archive

Run it with:

```bash
python basic_usage.py
```

## Requirements

These examples require:

1. The MimeArchiveFS package to be installed or available in the parent directory
2. For the CLI example: `pip install fire rich`

## Additional Resources

For more information, see:
- [MimeArchiveFS README](../README.md)
- [API Documentation](https://github.com/example/mimearchivefs/docs) 