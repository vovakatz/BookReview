import os
from typing import List
from openai import OpenAI
import json

from book_processor import analyze_book, generate_comparative_report
from models.book import Book
from utils.epub_to_text import extract_text_from_epub
from utils.files import get_files, extract_book_info
from utils.pdf_to_text import extract_text_from_pdf
from utils.xml_to_text import extract_text_from_xml


def main():
    # Initialize OpenAI client
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )

    files: List[str] = get_files("./books")
    books: List[Book] = []

    for file in files:
        if file.endswith(".epub"):
            content = extract_text_from_epub(file)
        elif file.endswith(".xml"):
            content = extract_text_from_xml(file)
        elif file.endswith(".pdf"):
            content = extract_text_from_pdf(file)
        else:
            raise ValueError(f"Cannot process file.  Unrecognized format: {file}")

        author, title = extract_book_info(file)
        books.append(Book(
            title = title,
            author = author,
            content=content
        ))


    # Analyze each book in its entirety
    analyses = {}
    for book in books:
        analyses[book.title] = analyze_book(client, book)

    # Generate comparative report
    report = generate_comparative_report(client, analyses)

    # Save analyses and report
    with open('book_analyses.json', 'w') as f:
        json.dump(analyses, f, indent=2)

    with open('isolation_analysis.txt', 'w') as f:
        f.write(report)

    print("Done")


if __name__ == "__main__":
    main()