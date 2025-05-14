from pathlib import Path
from typing import List


def load_photo_paths(path: str) -> List[str]:
    """
    Load paths to all photos from the given directory.

    This function checks if the provided path is a directory and if so,
    returns a list of paths to all photos within it. Supported photo extensions
    are: .jpg, .jpeg, .png.

    Args:
        path (str): Path to the directory containing photos

    Returns:
        List[str]: List of absolute paths to photos

    Raises:
        NotADirectoryError: If the provided path is not a directory
        FileNotFoundError: If the directory does not exist

    Example:
        >>> photo_paths = load_photo_paths("path/to/photos")
        >>> print(len(photo_paths))
        >>> print(photo_paths[0])  # prints first photo path
    """
    photo_dir = Path(path)

    if not photo_dir.exists():
        raise FileNotFoundError(f"Directory does not exist: {path}")

    if not photo_dir.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")

    photo_extensions = {".jpg", ".jpeg", ".png"}

    photo_paths = [
        str(file.absolute())
        for file in photo_dir.iterdir()
        if file.is_file() and file.suffix.lower() in photo_extensions
    ]

    return photo_paths
