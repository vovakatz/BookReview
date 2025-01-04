import json
import time
from typing import Dict, List

from openai import OpenAI
from models.book import Book


def analyze_book(client: OpenAI, book: Book) -> Dict:
    """Analyze an entire book by processing it in chunks."""
    print(f"Starting analysis of {book.title}...")

    chunks = chunk_text(book.content, max_chunk_size=16000)
    print(f"Split {book.title} into {len(chunks)} chunks")

    chunk_analyses = []
    for i, chunk in enumerate(chunks):
        print(f"Analyzing chunk {i + 1}/{len(chunks)} of {book.title}")
        analysis = analyze_isolation_themes(client, chunk)
        if analysis:
            chunk_analyses.append(analysis)
        time.sleep(1)  # Rate limiting

    return combine_analyses(chunk_analyses)

def chunk_text(text: str, max_chunk_size: int = 3000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks for processing."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chunk_size
        if end > len(text):
            end = len(text)
        # Try to find a proper sentence end for cleaner chunks
        if end < len(text):
            for i in range(end, max(start + max_chunk_size - 500, start), -1):
                if text[i-1] in '.!?' and text[i:i+1].isspace():
                    end = i
                    break
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks


def analyze_isolation_themes(client: OpenAI, text_chunk: str, retry_count: int = 3) -> Dict:
    """Analyze themes of social isolation in a text chunk using OpenAI's API."""

    prompt = """Analyze how social isolation is portrayed in this text excerpt. Focus on:
    1. Specific manifestations of isolation
    2. The character's relationship with isolation
    3. The author's perspective on isolation
    4. Key quotes that demonstrate isolation

    Provide your analysis in JSON format with these keys:
    {
        "manifestations": [],
        "character_relationship": "",
        "author_perspective": "",
        "key_quotes": []
    }"""

    for attempt in range(retry_count):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini", # using gpt-4o-mini for efficiency
                messages=[
                    {"role": "system", "content": "You are a literary analyst focused on themes of social isolation."},
                    {"role": "user", "content": f"{prompt}\n\nText: {text_chunk}"}
                ],
                temperature=0.7
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            if attempt == retry_count - 1:
                print(f"Failed to analyze chunk after {retry_count} attempts: {e}")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff


def combine_analyses(chunk_analyses: List[Dict]) -> Dict:
    """Combine analyses from multiple chunks into a single analysis."""
    combined = {
        "manifestations": [],
        "character_relationship": "",
        "author_perspective": "",
        "key_quotes": []
    }

    manifestations_set = set()
    quotes_set = set()
    relationships = []
    perspectives = []

    for analysis in chunk_analyses:
        if not analysis:
            continue
        manifestations_set.update(analysis.get("manifestations", []))
        quotes_set.update(analysis.get("key_quotes", []))
        if analysis.get("character_relationship"):
            relationships.append(analysis["character_relationship"])
        if analysis.get("author_perspective"):
            perspectives.append(analysis["author_perspective"])

    combined["manifestations"] = list(manifestations_set)
    combined["key_quotes"] = list(quotes_set)
    combined["character_relationship"] = " ".join(relationships)
    combined["author_perspective"] = " ".join(perspectives)

    return combined


def generate_comparative_report(client: OpenAI, analyses: Dict[str, Dict]) -> str:
    """Generate a 5-paragraph comparative report."""

    prompt = """Write a 5-paragraph comparative analysis of how these books handle the theme of social isolation. The analysis should include:

    1. Introduction with a clear thesis about how these works approach isolation
    2. Analysis of the manifestations of isolation in each work
    3. Comparison of how the characters deal with their isolation
    4. Examination of the authors' perspectives on isolation
    5. Conclusion synthesizing the findings and their broader implications

    Include specific quotes and examples from each text.

    The analyses to compare are: {analyses}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a literary analyst writing a comparative essay."},
                {"role": "user", "content": prompt.format(analyses=json.dumps(analyses, indent=2))}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating report: {e}")
        return None