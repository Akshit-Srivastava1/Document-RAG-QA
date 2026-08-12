import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LLM_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHROMA_DB_PATH = "../chroma_db"
COLLECTION_NAME = "document_collection"

UPLOAD_FOLDER = "../uploads"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K = 3

ALLOWED_EXTENSIONS = [".pdf"]

LOG_LEVEL = "INFO"

PROJECT_NAME = "Document RAG QA"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = ("Upload PDF documents and ask questions using " "RAG, ChromaDB, FastAPI and Gemini.")