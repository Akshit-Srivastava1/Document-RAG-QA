# 📄 Document RAG QA

A full-stack **Document Question Answering application** built using **React, FastAPI, Sentence Transformers, ChromaDB, and Google Gemini**.

The application allows users to upload a PDF and ask questions about its content. It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from the document before generating an answer with an LLM.

---

## 🚀 Features

- 📄 PDF upload and page-wise text extraction
- 🧹 Text cleaning and preprocessing
- ✂️ Overlapping text chunking
- 🧠 Semantic embeddings using `all-MiniLM-L6-v2`
- 🗄️ Persistent ChromaDB vector storage
- 🔎 Semantic similarity search
- 🤖 Gemini-powered answer generation
- 📑 Source page references
- ⚡ FastAPI REST API
- 📚 Automatic Swagger/OpenAPI documentation
- 💬 React-based chat interface
- 🌐 CORS support for frontend/backend communication

---

## 🏗️ Architecture

```text
                    DOCUMENT INGESTION
                           │
                         PDF
                           │
                           ▼
                 PyMuPDF Text Extraction
                           │
                           ▼
                     Text Cleaning
                           │
                           ▼
                       Chunking
                  500 words / 100 overlap
                           │
                           ▼
                      Embeddings
                  all-MiniLM-L6-v2
                           │
                           ▼
                       ChromaDB
                    Vector Storage
                           │
                           │
            ───────────────┴───────────────
                           │
                           ▼
                     USER QUESTION
                           │
                           ▼
                    Query Embedding
                           │
                           ▼
                 ChromaDB Similarity Search
                           │
                           ▼
                  Top 3 Relevant Chunks
                           │
                           ▼
                    Context Building
                           │
                           ▼
                  Context + Question
                           │
                           ▼
                         Gemini
                           │
                           ▼
                  Answer + Source Pages