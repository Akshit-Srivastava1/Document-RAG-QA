import logging
import os
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_DESCRIPTION,
    UPLOAD_FOLDER,
    EMBEDDING_MODEL,
    LLM_MODEL,
)

from models import (
    UploadResponse,
    QuestionRequest,
    QuestionResponse,
)

from pdf_loader import extract_text
from chunking import chunk_text
from embedding import embed_documents
from vector_store import store_documents
from rag import ask_question

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    description=PROJECT_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(                            #This create the folder where uploaded PDFs will be stored
    UPLOAD_FOLDER,
    exist_ok=True
)

@app.on_event("startup")
def startup():
    logger.info("=" * 60)
    logger.info(f"{PROJECT_NAME} Started")
    logger.info(f"Embedding Model : {EMBEDDING_MODEL}")
    logger.info(f"LLM Model       : {LLM_MODEL}")
    logger.info("Vector Database : ChromaDB")
    logger.info("=" * 60)

@app.get(
    "/",
    tags=["Root"]
)
def root():
    return {
        "project": PROJECT_NAME,
        "version": PROJECT_VERSION,
        "framework": "FastAPI",
        "status": "Running"
    }

@app.get(
    "/health",
    tags=["Health"]
)
def health():

    return {
        "status": "healthy",
        "project": PROJECT_NAME,
        "embedding_model": EMBEDDING_MODEL,
        "llm": LLM_MODEL,
        "vector_database": "ChromaDB"
    }

@app.post(
    "/upload",
    response_model=UploadResponse,
    tags=["Document"],
    summary="Upload PDF",
    description="Upload a PDF, generate embeddings and store them in ChromaDB."
)
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )
        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Uploaded : {file.filename}")
        pages = extract_text(file_path)
        if not pages:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF contains no readable text."
            )
        logger.info(f"Pages Extracted : {len(pages)}")
        chunks = chunk_text(pages)
        logger.info(f"Chunks Created : {len(chunks)}")
        embedded_chunks = embed_documents(chunks)
        logger.info("Embeddings Generated")
        total_chunks = store_documents(embedded_chunks)
        logger.info("Embeddings Stored In ChromaDB")
        return UploadResponse(
            status="success",
            filename=file.filename,
            chunks=total_chunks,
            message="PDF uploaded and indexed successfully."
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post(                          
    "/ask",
    response_model=QuestionResponse,
    tags=["Question Answering"],
    summary="Ask Question",
    description="Ask questions from the uploaded PDF using Retrieval-Augmented Generation."
)
def ask(request: QuestionRequest):
    try:
        result = ask_question(request.question)
        return QuestionResponse(
            answer=result["answer"],
            source_pages=result["source_pages"]
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )