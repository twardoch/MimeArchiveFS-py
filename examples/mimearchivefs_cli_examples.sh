#!/bin/bash
# this_file: examples/mimearchivefs_cli_examples.sh
# Examples of using MimeArchiveFS from shell scripts
#
# To make this script executable:
#   chmod +x mimearchivefs_cli_examples.sh
#
# Run with:
#   ./mimearchivefs_cli_examples.sh

# Exit on error
set -e

# Set up basic variables
EXAMPLE_DIR=$(mktemp -d)
SOURCE_DIR="${EXAMPLE_DIR}/source"
EXTRACT_DIR="${EXAMPLE_DIR}/extract"
ARCHIVE_PATH="${EXAMPLE_DIR}/example.mht"
ARCHIVE2_PATH="${EXAMPLE_DIR}/example2.mht"

echo "Working in temporary directory: ${EXAMPLE_DIR}"

# Create test directories
mkdir -p "${SOURCE_DIR}/dir1/dir2"
mkdir -p "${EXTRACT_DIR}"

# Create some test files
echo "Hello, world!" >"${SOURCE_DIR}/file1.txt"
echo "This is in a subdirectory" >"${SOURCE_DIR}/dir1/file2.txt"
echo "This is in a nested subdirectory" >"${SOURCE_DIR}/dir1/dir2/file3.txt"
dd if=/dev/urandom bs=1024 count=10 of="${SOURCE_DIR}/binary.dat" 2>/dev/null

echo "=== Created test files in ${SOURCE_DIR} ==="
ls -la "${SOURCE_DIR}"
ls -la "${SOURCE_DIR}/dir1"
ls -la "${SOURCE_DIR}/dir1/dir2"
echo

# Example 1: Pack a folder into an MHT archive
echo "=== Example 1: Packing a folder ==="
echo "This example demonstrates how to create a new MHT archive and add files"
echo "from a directory structure, preserving paths."
echo
python3 -c "
import os
import sys
from mimearchivefs import MimeArchiveFileSystem

# Create a new archive in write mode
fs = MimeArchiveFileSystem('${ARCHIVE_PATH}', mode='w')

# Recursively add all files from the source directory
for root, dirs, files in os.walk('${SOURCE_DIR}'):
    for file in files:
        file_path = os.path.join(root, file)
        # Calculate the relative path for the archive
        rel_path = os.path.relpath(file_path, '${SOURCE_DIR}')
        
        # Read the file content
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Add to the archive
        fs.pipe_file(rel_path, content)
        print(f'Added {rel_path} to archive')

# Save the archive
fs.save()
print(f'Archive saved to ${ARCHIVE_PATH}')
"

# Example 2: Listing contents of an archive
echo
echo "=== Example 2: Listing archive contents ==="
echo "This example shows how to list files in an archive, both at the root level"
echo "and recursively through all directories."
echo
python3 -c "
from mimearchivefs import MimeArchiveFileSystem

# Open the archive
fs = MimeArchiveFileSystem('${ARCHIVE_PATH}')

# List files in the root
print('Files in root:')
root_files = fs.ls()
for file in root_files:
    print(f'  {file}')

# List files recursively
print('\nAll files (recursive):')
all_files = []
def list_recursive(path=''):
    if not path:
        items = fs.ls()
    else:
        items = fs.ls(path)
    
    for item in items:
        full_path = f'{path}/{item}' if path else item
        if fs.info(full_path)['type'] == 'directory':
            list_recursive(full_path)
        else:
            all_files.append(full_path)

list_recursive()
for file in sorted(all_files):
    info = fs.info(file)
    print(f'  {file} ({info[\"size\"]} bytes)')
"

# Example 3: Unpacking an archive
echo
echo "=== Example 3: Unpacking an archive ==="
echo "This example demonstrates how to extract all files from an archive"
echo "while preserving the directory structure."
echo
python3 -c "
from mimearchivefs import MimeArchiveFileSystem
import os

# Open the archive
fs = MimeArchiveFileSystem('${ARCHIVE_PATH}')

# Function to extract files recursively
def extract_recursive(fs, path='', extract_dir='${EXTRACT_DIR}'):
    if not path:
        items = fs.ls()
    else:
        items = fs.ls(path)
    
    for item in items:
        full_path = f'{path}/{item}' if path else item
        target_path = os.path.join(extract_dir, full_path)
        
        if fs.info(full_path)['type'] == 'directory':
            os.makedirs(target_path, exist_ok=True)
            extract_recursive(fs, full_path, extract_dir)
        else:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Extract the file
            with fs.open(full_path, 'rb') as src, open(target_path, 'wb') as dst:
                dst.write(src.read())
            print(f'Extracted: {full_path} -> {target_path}')

extract_recursive(fs)
print(f'All files extracted to ${EXTRACT_DIR}')
"

# Example 4: Using the MimeArchive (ZipFile-like) API for unpacking
echo
echo "=== Example 4: Using MimeArchive API to unpack ==="
echo "This example shows how to use the ZipFile-like API (MimeArchive)"
echo "to easily extract files from an archive."
echo
python3 -c "
import sys
# Add the module in development to path if needed
sys.path.insert(0, 'src')

from mimearchivefs.archive import MimeArchive

# Open the archive
with MimeArchive('${ARCHIVE_PATH}') as archive:
    # Print directory listing
    print('Archive contains:')
    archive.printdir()
    
    # Extract all files
    archive.extractall('${EXTRACT_DIR}/archive')
    print(f'Files extracted to ${EXTRACT_DIR}/archive')
"

# Example 5: Adding files to an existing archive
echo
echo "=== Example 5: Adding files to an existing archive ==="
echo "This example demonstrates how to open an existing archive in append mode"
echo "and add new files to it."
echo
python3 -c "
from mimearchivefs import MimeArchiveFileSystem

# Open the archive in append mode
fs = MimeArchiveFileSystem('${ARCHIVE_PATH}', mode='a')

# Add a new file
new_content = 'This is a new file added to the existing archive.'
fs.pipe_file('new_file.txt', new_content)
print('Added new_file.txt to the archive')

# Add a new file in a directory
fs.pipe_file('dir1/new_file2.txt', 'This is another new file in dir1.')
print('Added dir1/new_file2.txt to the archive')

# Save changes
fs.save()
print('Archive updated')

# Verify the new files
fs = MimeArchiveFileSystem('${ARCHIVE_PATH}')
print('\nUpdated archive contents:')
all_files = []
def list_recursive(path=''):
    if not path:
        items = fs.ls()
    else:
        items = fs.ls(path)
    
    for item in items:
        full_path = f'{path}/{item}' if path else item
        if fs.info(full_path)['type'] == 'directory':
            list_recursive(full_path)
        else:
            all_files.append(full_path)

list_recursive()
for file in sorted(all_files):
    info = fs.info(file)
    print(f'  {file} ({info[\"size\"]} bytes)')
"

# Example 6: Removing a file from an archive
echo
echo "=== Example 6: Removing a file from an archive ==="
echo "This example shows how to remove files from an existing archive."
echo
python3 -c "
from mimearchivefs import MimeArchiveFileSystem

# Open the archive in append mode (or read-write mode)
fs = MimeArchiveFileSystem('${ARCHIVE_PATH}', mode='a')

# Remove a file
fs.rm_file('new_file.txt')
print('Removed new_file.txt from the archive')

# Save changes
fs.save()
print('Archive updated')

# Verify the file was removed
fs = MimeArchiveFileSystem('${ARCHIVE_PATH}')
print('\nArchive contents after removal:')
all_files = []
def list_recursive(path=''):
    if not path:
        items = fs.ls()
    else:
        items = fs.ls(path)
    
    for item in items:
        full_path = f'{path}/{item}' if path else item
        if fs.info(full_path)['type'] == 'directory':
            list_recursive(full_path)
        else:
            all_files.append(full_path)

list_recursive()
for file in sorted(all_files):
    print(f'  {file}')
"

# Example 7: Copying files from one archive to another
echo
echo "=== Example 7: Copying files between archives ==="
echo "This example demonstrates how to copy specific files from one archive to another."
echo
python3 -c "
from mimearchivefs import MimeArchiveFileSystem

# Create a new target archive
target_fs = MimeArchiveFileSystem('${ARCHIVE2_PATH}', mode='w')

# Open the source archive
source_fs = MimeArchiveFileSystem('${ARCHIVE_PATH}')

# Find all files in the source archive
all_files = []
def list_recursive(fs, path=''):
    if not path:
        items = fs.ls()
    else:
        items = fs.ls(path)
    
    for item in items:
        full_path = f'{path}/{item}' if path else item
        if fs.info(full_path)['type'] == 'directory':
            list_recursive(fs, full_path)
        else:
            all_files.append(full_path)

list_recursive(source_fs)

# Copy each file
for file_path in all_files:
    if 'dir1/dir2' in file_path:  # Only copy files from dir1/dir2
        # Read from source
        content = source_fs.cat_file(file_path)
        
        # Write to target with the same path
        target_fs.pipe_file(file_path, content)
        print(f'Copied {file_path} to new archive')

# Save the target archive
target_fs.save()
print(f'Created new archive with selected files at ${ARCHIVE2_PATH}')

# Verify the new archive contents
target_fs = MimeArchiveFileSystem('${ARCHIVE2_PATH}')
print('\nNew archive contents:')
target_files = []
list_recursive(target_fs)
for file in sorted(target_files):
    info = target_fs.info(file)
    print(f\"  {file} ({info['size']} bytes)\")
"

# Clean up
echo
echo "=== Cleaning up ==="
echo "Temporary files are in: ${EXAMPLE_DIR}"
echo "To clean up, run: rm -rf ${EXAMPLE_DIR}"

echo
echo "Examples completed! Use these patterns in your own scripts to work with MimeArchiveFS."
echo "For more information, see the MimeArchiveFS documentation or run 'python mimearchivefs_cli.py --help'."
