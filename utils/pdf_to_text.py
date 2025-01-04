from pathlib import Path
import PyPDF2
import io

def extract_text_from_pdf(source):
    """
    Extract text content from a PDF file.
    """
    try:
        # Handle different input types
        if isinstance(source, (str, Path)):
            pdf_file = open(source, 'rb')
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