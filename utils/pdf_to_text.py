from pathlib import Path
import PyPDF2
import io

def extract_text_from_pdf(source):
    """
    Extract text content from a PDF file.

    Args:
        source: The PDF source - can be a file path (str/Path), bytes, or BytesIO object

    Returns:
        str: Extracted text content
    """
    try:
        # Handle different input types
        if isinstance(source, (str, Path)):
            pdf_file = open(source, 'rb')
        elif isinstance(source, bytes):
            pdf_file = io.BytesIO(source)
        elif isinstance(source, io.BytesIO):
            pdf_file = source
        else:
            raise ValueError(f"Unsupported source type: {type(source)}")

        # Create PDF reader and extract text
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        # Close file if we opened it
        if isinstance(source, (str, Path)):
            pdf_file.close()

        return text.strip()

    except Exception as e:
        raise ValueError(f"Error processing PDF: {str(e)}")