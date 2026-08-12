from typing import List, Dict
import uuid
import chromadb
from chromadb.config import Settings

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME
)
client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH,
    settings=Settings(anonymized_telemetry=False)
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

def clear_collection() -> None:
    """
    Remove all existing vectors.
    """
    try:
        ids = collection.get()["ids"]
        if ids:
            collection.delete(ids=ids)
    except Exception:
        pass

def store_documents(chunks: List[Dict]) -> int:

    """
    Store embeddings in ChromaDB.

    Returns
    -------
    int
        Number of stored chunks.
    """

    clear_collection()
    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        ids.append(str(uuid.uuid4()))
        documents.append(
            chunk["text"]
        )
        embeddings.append(
            chunk["embedding"]
        )
        metadatas.append(
            {
                "page": chunk["page"]
            }
        )
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    return len(ids)

def search_documents(query_embedding: List[float],top_k: int = 3) -> List[Dict]:

    """
    Perform semantic similarity search.
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        retrieved_chunks.append(
            {
                "page": metadata["page"],
                "text": document,
                "score": round(distance, 4)
            }
        )
    return retrieved_chunks