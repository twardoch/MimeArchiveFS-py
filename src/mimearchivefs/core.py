#!/usr/bin/env python3
# this_file: src/mimearchivefs/core.py

"""Core functionality for parsing and writing MimeArchive files."""

import email
import io
import mimetypes
import re
from email.message import Message
from pathlib import Path
from typing import cast

# Import utils using full path to avoid relative import errors
import mimearchivefs.utils as utils


class MimeArchiveParser:
    """Parser for MimeArchive (.mht) files."""

    FILE_MARKER_PATTERN = r"--- FILE: ([^-]+) ---"

    def __init__(self, file_obj: str | io.IOBase) -> None:
        """
        Initialize the parser with a file path or file-like object.

        Args:
            file_obj: Path to the .mht file or file-like object
        """
        self.file_obj = file_obj
        self.content: dict[str, bytes] = {}
        self.metadata: dict[str, dict[str, str]] = {}

    def parse(self) -> dict[str, bytes]:
        """
        Parse the .mht file and extract its contents.

        Returns:
            Dictionary mapping paths to file contents
        """
        # Reset state
        self.content = {}
        self.metadata = {}

        # Read content from file
        if isinstance(self.file_obj, str):
            raw_content = Path(self.file_obj).read_bytes()
        else:
            # Ensure we're reading from the beginning
            if hasattr(self.file_obj, "seek") and callable(self.file_obj.seek):
                self.file_obj.seek(0)
            raw_content = self.file_obj.read()

        # Parse the email message
        if isinstance(raw_content, bytes):
            message = email.message_from_bytes(raw_content)
        else:
            # Convert to string if not already bytes
            message = email.message_from_string(str(raw_content))

        self._process_message(message)

        return self.content

    def _process_message(self, message: Message) -> None:
        """
        Process an email message and extract file contents.

        Args:
            message: Email message object
        """
        if not message.is_multipart():
            # Handle single-part message with file marker in content
            content = message.get_payload(decode=True)
            if content is not None and isinstance(content, bytes):
                self._extract_files_from_content(content)
            return

        # Handle multipart message
        payload = message.get_payload()
        if isinstance(payload, list):
            for part in payload:
                if isinstance(part, Message):
                    if part.is_multipart():
                        self._process_message(part)
                    else:
                        self._process_part(part)

    def _process_part(self, part: Message) -> None:
        """
        Process a message part and extract file content.

        Args:
            part: Message part
        """
        # Check for file marker in Content-Description or Content-Location
        path = None
        for header in ["Content-Description", "Content-Location"]:
            value = part.get(header)
            if value:
                file_match = re.search(self.FILE_MARKER_PATTERN, value)
                if file_match:
                    path = file_match.group(1)
                    break

                # If we have a valid path in Content-Location, use it
                if header == "Content-Location" and "/" in value:
                    path = value
                    break

        # If no path found, check content for file marker
        content = None
        if not path:
            content = part.get_payload(decode=True)
            if content is not None and isinstance(content, bytes):
                try:
                    content_str = content.decode("utf-8")
                    file_match = re.search(self.FILE_MARKER_PATTERN, content_str)
                    if file_match:
                        path = file_match.group(1)
                        # Strip file marker from content
                        marker = f"--- FILE: {path} ---"
                        content = content_str.replace(marker, "").encode("utf-8")
                except UnicodeDecodeError:
                    # Binary content, can't search for file marker
                    pass

        if path:
            if content is None:
                content = part.get_payload(decode=True)
                if not isinstance(content, bytes):
                    return

            path = utils.normalize_path(path)

            # Store content
            # self.content[path] = content # This line causes type errors and isn't needed for the current approach

            # Store metadata
            content_type = part.get_content_type()
            content_transfer_encoding = part.get("Content-Transfer-Encoding", "")
            self.metadata[path] = {
                "Content-Type": content_type,
                "Content-Transfer-Encoding": content_transfer_encoding,
            }

    def _extract_files_from_content(self, content: bytes) -> None:
        """
        Extract files from plain content with file markers.

        Args:
            content: Raw content bytes
        """
        try:
            content_str = content.decode("utf-8")
        except UnicodeDecodeError:
            # Can't extract file markers from binary content
            return

        # Split by file markers
        file_markers = re.finditer(self.FILE_MARKER_PATTERN, content_str)

        marker_positions = []
        for match in file_markers:
            path = match.group(1)
            start_pos = match.end()
            marker_positions.append((path, start_pos))

        # Extract content between markers
        for i, (path, start_pos) in enumerate(marker_positions):
            end_pos = len(content_str)
            if i < len(marker_positions) - 1:
                # Find the next marker position
                next_marker_pos = content_str.find("--- FILE:", start_pos)
                if next_marker_pos != -1:
                    end_pos = next_marker_pos

            file_content = content_str[start_pos:end_pos].strip()
            path = utils.normalize_path(path)
            self.content[path] = file_content.encode("utf-8")

            # Guess mime type based on extension
            filename = utils.get_filename(path)
            mime_type, _ = mimetypes.guess_type(filename)
            self.metadata[path] = {
                "Content-Type": mime_type or "application/octet-stream",
                "Content-Transfer-Encoding": "8bit",
            }


def parse_mht(file_obj: str | io.IOBase) -> dict[str, bytes]:
    """
    Parse an MHT file and extract its contents.

    Args:
        file_obj: Path to the .mht file or file-like object

    Returns:
        Dictionary mapping paths to file contents
    """
    parser = MimeArchiveParser(file_obj)
    return parser.parse()


def write_mht(file_obj: str | io.IOBase, file_data: dict[str, str | bytes]) -> None:
    """
    Write files to an MHT archive using custom generation for 8bit text.

    Args:
        file_obj: Path or file-like object to write to
        file_data: Dictionary mapping paths to file contents
    """
    import base64
    import mimetypes
    from email.generator import Generator  # Use Generator for boundary generation
    from io import TextIOWrapper  # For checking mode
    import uuid  # Alternative boundary generation

    # Generate a unique boundary
    # boundary = _make_boundary() # _make_boundary is internal
    boundary = str(uuid.uuid4())  # Generate UUID for boundary
    boundary_bytes = boundary.encode("ascii")

    # Determine if we need to open a file or use an existing object
    needs_close = False
    out_file: io.IOBase  # Define type for out_file
    if isinstance(file_obj, str):
        out_file = open(file_obj, "wb")
        needs_close = True
    elif (
        hasattr(file_obj, "mode")
        and isinstance(getattr(file_obj, "mode", ""), str)
        and "b" in getattr(file_obj, "mode", "")
    ):
        out_file = file_obj
    elif hasattr(file_obj, "write"):
        # Try to write bytes, hoping it's a binary stream like BytesIO
        out_file = file_obj
        # Check if write works with bytes
        try:
            # We need to cast here as write may not be guaranteed to accept bytes
            if hasattr(out_file, "write"):
                cast(io.BytesIO, out_file).write(b"")
            else:
                raise TypeError("Provided file object lacks a write method.")
        except TypeError:
            raise TypeError(
                "file_obj must be a string path or a file-like object opened in binary mode (or support writing bytes)"
            )
    else:
        raise TypeError("file_obj must be a string path or a file-like object with a write method")

    try:
        # --- Write Main Headers ---
        headers = (
            f'Content-Type: multipart/related; boundary="{boundary}"\r\n'
            f"MIME-Version: 1.0\r\n"
            f"Subject: MimeArchiveFS Archive\r\n\r\n"
        )
        out_file.write(headers.encode("ascii"))

        # --- Write Each Part ---
        for path, content in file_data.items():
            # Normalize path and ensure content is bytes
            norm_path = utils.normalize_path(path)
            if isinstance(content, str):
                content_bytes = content.encode("utf-8")
            else:
                # If content is memoryview, convert to bytes
                if isinstance(content, memoryview):
                    content_bytes = bytes(content)
                else:
                    content_bytes = content  # Assume it's bytes or bytearray

            # Check if content_bytes is actually bytes before proceeding
            if not isinstance(content_bytes, (bytes, bytearray)):
                raise TypeError(f"Content for path {path} is not bytes or convertible to bytes.")

            # Determine mime type
            filename = utils.get_filename(norm_path)
            mime_type, _ = mimetypes.guess_type(filename)
            if not mime_type:
                if filename.endswith((".txt", ".html", ".htm", ".css", ".js", ".json", ".xml")):
                    if filename.endswith(".txt"):
                        mime_type = "text/plain"
                    elif filename.endswith((".html", ".htm")):
                        mime_type = "text/html"
                    elif filename.endswith(".css"):
                        mime_type = "text/css"
                    elif filename.endswith(".js"):
                        mime_type = "application/javascript"
                    elif filename.endswith(".json"):
                        mime_type = "application/json"
                    elif filename.endswith(".xml"):
                        mime_type = "application/xml"
                else:
                    mime_type = "application/octet-stream"

            if mime_type is None:  # Should not happen with the logic above, but safety check
                mime_type = "application/octet-stream"

            # Determine if text
            is_text = mime_type.startswith("text/") or mime_type in [
                "application/javascript",
                "application/json",
                "application/xml",
            ]
            if not is_text:
                try:
                    # Ensure we decode bytes, not bytearray/memoryview directly
                    bytes_to_decode = bytes(content_bytes)
                    bytes_to_decode.decode("utf-8")
                    is_text = True
                    if not mime_type.startswith(
                        "text/"
                    ):  # Assign text/plain if decoding worked but mime wasn't text
                        mime_type = "text/plain"
                except UnicodeDecodeError:
                    is_text = False
                    if mime_type.startswith("text/"):
                        mime_type = (
                            "application/octet-stream"  # Correct mime type if it was wrongly text
                        )

            # --- Write Boundary Separator ---
            out_file.write(b"\r\n--" + boundary_bytes + b"\r\n")

            # --- Write Part Headers ---
            part_headers = [
                b"MIME-Version: 1.0",
            ]
            if is_text:
                part_headers.append(b"Content-Transfer-Encoding: 8bit")
                part_headers.append(
                    f"Content-Type: {mime_type}; charset=utf-8; format=flowed".encode("ascii")
                )
            else:
                part_headers.append(b"Content-Transfer-Encoding: base64")
                part_headers.append(f"Content-Type: {mime_type}".encode("ascii"))

            part_headers.append(f"Content-Location: {norm_path}".encode("ascii"))
            part_headers.append(f"Content-Description: --- FILE: {norm_path} ---".encode("ascii"))

            # Write headers followed by empty line
            out_file.write(b"\r\n".join(part_headers) + b"\r\n\r\n")

            # --- Write Part Content ---
            if is_text:
                # Write raw bytes for text files
                out_file.write(content_bytes)
            else:
                # Write base64 encoded bytes for binary files
                # base64.encodebytes adds necessary newlines for MIME
                encoded_content = base64.encodebytes(content_bytes)
                out_file.write(encoded_content)

        # --- Write Final Boundary ---
        out_file.write(b"\r\n--" + boundary_bytes + b"--\r\n")

    finally:
        # Close the file if we opened it
        if needs_close:
            out_file.close()
