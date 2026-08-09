from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL  # pyrefly: ignore [missing-import]

class Embedder:
    def __init__(self):
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, query):
        return self.model.encode(query).tolist()
