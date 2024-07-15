import os
import tempfile
from pathlib import Path


def create_temp_file(suffix: str) -> Path:
    """
    Create a temporary file with the given suffix.

    Args:
        suffix (str): The file extension (e.g., '.mp3', '.wav')

    Returns:
        Path: Path to the created temporary file.
    """
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
        return Path(temp_file.name)


def cleanup_temp_files(files: list[Path]) -> None:
    """
    Clean up temporary files.

    Args:
        files (list[Path]): List of temporary file paths to be removed.
    """
    for file in files:
        try:
            os.remove(file)
        except OSError as e:
            print(f"Error deleting temporary file {file}: {e}")
