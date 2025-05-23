import os
import uuid
from typing import Set, Optional, Tuple
from werkzeug.datastructures import FileStorage

# Maximum file size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


def validate_file(
    file: FileStorage, allowed_extensions: Set[str], max_size: int = MAX_FILE_SIZE
) -> Tuple[bool, Optional[str]]:
    """
    Validate a file upload.

    Args:
        file: The uploaded file
        allowed_extensions: Set of allowed file extensions
        max_size: Maximum file size in bytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"

    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer

    if file_size > max_size:
        return False, f"File too large. Maximum size is {max_size / 1024 / 1024:.1f} MB"

    # Check file extension
    if "." not in file.filename:
        return False, "Invalid filename"

    extension = file.filename.rsplit(".", 1)[1].lower()
    if extension not in allowed_extensions:
        return (
            False,
            f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}",
        )

    # Additional content type validation could be added here
    # For example, checking magic numbers for file types

    return True, None


def secure_filename(filename: str) -> str:
    """
    Generate a secure filename for storage.

    Args:
        filename: The original filename

    Returns:
        A secure filename with a UUID prefix
    """
    if not filename:
        return ""

    # Get the file extension
    if "." in filename:
        extension = filename.rsplit(".", 1)[1].lower()
    else:
        extension = ""

    # Generate a UUID for the filename
    safe_name = f"{uuid.uuid4().hex}"

    # Add the extension if it exists
    if extension:
        safe_name = f"{safe_name}.{extension}"

    return safe_name
