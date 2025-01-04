import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text_from_epub(epub_path: str) -> str:
    """Extract plain text from EPUB file."""
    book = epub.read_epub(epub_path)
    text = ""

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text += soup.get_text() + "\n"

    # Clean up the text
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


