from xml.etree import ElementTree
import re


def extract_text_from_xml(source):
    """
    Extract pure text content from XML, ignoring all tags and attributes.
    """
    try:

        tree = ElementTree.parse(source)
        root = tree.getroot()

        # Get all text recursively
        text_parts = []
        for elem in root.iter():
            if elem.text:
                text_parts.append(elem.text.strip())
            if elem.tail:
                text_parts.append(elem.tail.strip())

        # Join all parts and normalize whitespace
        text = ' '.join(text_parts)
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    except Exception as e:
        raise ValueError(f"Error processing XML: {str(e)}")