import pytest
import uuid
from src.vector_store import VectorStore

def test_vector_store_operations():
    vs = VectorStore()
    initial_count = vs.count()
    assert isinstance(initial_count, int)

    # Mock doküman verileri
    test_id = str(uuid.uuid4())
    test_doc = "Bu bir test dokümanıdır. Yatırım ve sermaye piyasaları ile ilgilidir."
    test_embedding = [0.1] * 1024
    test_meta = {"source": "test_doc.txt", "chunk_index": 0}

    # Doküman ekleme
    vs.add_documents(
        documents=[test_doc],
        embeddings=[test_embedding],
        metadatas=[test_meta],
        ids=[test_id]
    )

    # Eklenen doküman sonrası sayı kontrolü
    new_count = vs.count()
    assert new_count == initial_count + 1

    # Sorgulama (Query) testi
    results = vs.query(query_embeddings=[test_embedding], n_results=1)
    assert "documents" in results
    assert len(results["documents"][0]) > 0
    assert results["documents"][0][0] == test_doc

    # Temizlik (Delete)
    vs.delete_documents(ids=[test_id])
    assert vs.count() == initial_count
