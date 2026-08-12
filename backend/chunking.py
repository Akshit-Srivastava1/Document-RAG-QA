from typing import List, Dict
from config import (CHUNK_SIZE, CHUNK_OVERLAP)

def chunk_text(pages: List[Dict], chunk_size: int = 500, overlap: int = 100) -> List[Dict]:
    """
    Split extracted text into overlapping chunks.

    Parameters:
        pages       : Output from pdf_loader.py
        chunk_size  : Maximum words in a chunk
        overlap     : Number of overlapping words

    Returns:
        [
            {   
                "page": 1,
                "text": "..."
            }
        ]
    """

    chunks = []
    for page in pages:
        words = page["text"].split()
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)
            if chunk_text.strip():
                chunks.append(
                    {
                        "page": page["page"],
                        "text": chunk_text
                    }
                )
            start += chunk_size - overlap
    return chunks