import os
import glob
import uuid
from pypdf import PdfReader

from src.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.embedding import Embedder
from src.vector_store import VectorStore

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "documents")

def read_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text

def read_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT {file_path}: {e}")
        return ""

def chunk_text(text, chunk_size, chunk_overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def ingest_documents():
    if not os.path.exists(DOCS_DIR):
        print(f"Documents directory not found at {DOCS_DIR}")
        return

    # Find all pdf and txt files
    pdf_files = glob.glob(os.path.join(DOCS_DIR, "**", "*.pdf"), recursive=True)
    txt_files = glob.glob(os.path.join(DOCS_DIR, "**", "*.txt"), recursive=True)
    all_files = pdf_files + txt_files

    if not all_files:
        print("No documents found to ingest.")
        return

    # Initialize modular components
    embedder = Embedder()
    vector_store = VectorStore()

    for file_path in all_files:
        print(f"Processing {file_path}...")
        
        # 1. Read document
        if file_path.endswith(".pdf"):
            text = read_pdf(file_path)
        else:
            text = read_txt(file_path)
            
        if not text.strip():
            print(f"No text extracted from {file_path}. Skipping.")
            continue
            
        # 2. Chunk text
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        print(f"Created {len(chunks)} chunks for {os.path.basename(file_path)}")
        
        if not chunks:
            continue
            
        # 3. Vectorize chunks using Embedder
        embeddings = embedder.embed_documents(chunks)
        
        # 4. Store in ChromaDB using VectorStore
        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        metadatas = [{"source": os.path.basename(file_path), "chunk_index": i} for i in range(len(chunks))]
        
        vector_store.add_documents(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully ingested {os.path.basename(file_path)}\n")

if __name__ == "__main__":
    print("Starting ingestion process...")
    ingest_documents()
    print("Ingestion complete!")
