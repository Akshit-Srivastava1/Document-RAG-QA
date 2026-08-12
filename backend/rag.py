from typing import Dict, List
import google.generativeai as genai
from embedding import embed_query
from vector_store import search_documents
from config import (GEMINI_API_KEY, LLM_MODEL, TOP_K)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(LLM_MODEL)

def build_context(chunks: List[Dict]) -> str:
    """
    Convert retrieved chunks into context.
    """
    context = ""
    for chunk in chunks:
        context += (
            f"\n\n"
            f"Page: {chunk['page']}\n"
            f"{chunk['text']}"
        )
    return context

def ask_question(question: str) -> Dict:
    """
    Complete RAG Pipeline.

    1. Embed user question
    2. Retrieve similar chunks
    3. Build context
    4. Send to Gemini
    5. Return answer
    """
    query_embedding = embed_query(question)
    retrieved_chunks = search_documents(query_embedding=query_embedding, top_k=TOP_K)
    if len(retrieved_chunks) == 0:
        return {
            "answer": "No relevant information found.",
            "source_pages": []
        }
    context = build_context(retrieved_chunks)
    prompt = f"""
You are a professional document question-answering assistant.

Rules:

1. Answer ONLY using the provided context.

2. Never make up information.

3. If information is unavailable, reply exactly:

"I couldn't find this information in the uploaded document."

4. Give a concise and accurate answer.

5. Mention the important points clearly.

Context:

{context}

Question:

{question}

Answer:
"""
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        raise Exception(f"Gemini Error: {str(e)}")
    pages = sorted(list(set(chunk["page"] for chunk in retrieved_chunks)))
    return {
        "answer": response.text.strip(),
        "source_pages": pages
    }