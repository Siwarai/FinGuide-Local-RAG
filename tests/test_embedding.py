import pytest
from src.embedding import Embedder  # pyrefly: ignore [missing-import]
from src.config import EMBEDDING_DIM  # pyrefly: ignore [missing-import]

def test_embedder_query():
    embedder = Embedder()
    vec = embedder.embed_query("Finansal okuryazarlık")
    assert isinstance(vec, list)
    assert len(vec) == EMBEDDING_DIM

def test_embedder_documents():
    embedder = Embedder()
    docs = ["Hisse senedi nedir?", "Tahvil bir borçlanma aracıdır."]
    vecs = embedder.embed_documents(docs)
    assert len(vecs) == 2
    assert len(vecs[0]) == EMBEDDING_DIM
