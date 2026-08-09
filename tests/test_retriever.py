import pytest
from src.retriever import Retriever  # pyrefly: ignore [missing-import]
from src.config import MIN_RETRIEVAL_SCORE  # pyrefly: ignore [missing-import]

def test_retriever_initialization():
    retriever = Retriever()
    assert retriever.embedder is not None
    assert retriever.vector_store is not None

def test_retriever_matched_query():
    retriever = Retriever()
    # Bilgi tabanımızda yer alan bilinen bir kavram
    results = retriever.retrieve("Bileşik faiz nedir?", top_k=2)
    assert isinstance(results, list)
    if results:
        top_result = results[0]
        assert "chunk" in top_result
        assert "metadata" in top_result
        assert "score" in top_result
        assert top_result["score"] >= MIN_RETRIEVAL_SCORE

def test_retriever_unmatched_query_threshold():
    retriever = Retriever()
    # Bilgi tabanıyla tamamen alakasız bir soru
    results = retriever.retrieve("Mars gezegeninde oksijen oranı kaçtır?", min_score=0.95)
    assert results == []
