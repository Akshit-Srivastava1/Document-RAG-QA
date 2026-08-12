from typing import List, Dict
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def embed_documents(chunks: List[Dict]) -> List[Dict]:
    """
    Generate embeddings for document chunks.

    Args:
        chunks: List of dictionaries containing page number and text.

    Returns:
        List of dictionaries with embeddings.
    """

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True                       #It is useful for similarity search because the vectors are placed on a normalized scale, making cosine-based similarity comparisons more convenient.
    )

    embedded_chunks = []
    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            {
                "page": chunk["page"],
                "text": chunk["text"],
                "embedding": embedding.tolist()
            }
        )
    return embedded_chunks

def embed_query(query: str) -> List[float]:
    """
    Generate embedding for a user query.
    """
    embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embedding.tolist()