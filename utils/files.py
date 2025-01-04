from pathlib import Path
from typing import List, Union


def get_files(directory: Union[str, Path]) -> List[str]:
    directory = Path(directory)
    return [str(f.absolute()) for f in directory.iterdir() if f.is_file()]


def extract_book_info(file_path) -> (str,str):
    """
    Extract author name and book name from a file path.

    Args:
        file_path (str): Full path to the book file

    Returns:
        tuple: (author_name, book_name)
    """
    # Get just the filename from the path
    filename = file_path.split('/')[-1]

    # Remove the file extension
    name_without_extension = filename.rsplit('.', 1)[0]

    # Split by hyphen to separate author and book title
    author_name, book_name = name_without_extension.split('-', 1)

    return author_name.strip(), book_name.strip()

