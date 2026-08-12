import fitz
from typing import List, Dict

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing extra spaces
    and unnecessary line breaks.
    """
    text = text.replace("\n", " ")
    text = " ".join(text.split())

    return text

def extract_text(pdf_path: str) -> List[Dict]:
    """
    Extract page-wise text from a PDF.

    Returns:
    [
        {
            "page": 1,
            "text": "..."
        }
    ]
    """

    pages = []
    try:
        document = fitz.open(pdf_path)
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")
            text = clean_text(text)
            if not text:
                continue
            pages.append(
                {
                    "page": page_number,
                    "text": text
                }
            )
        document.close()
        return pages
    except Exception as e:
        raise Exception(f"PDF Extraction Error: {str(e)}")