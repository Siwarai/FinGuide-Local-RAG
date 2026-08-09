import pytest
from unittest.mock import patch
from src.rag import RAGPipeline, FALLBACK_MESSAGE  # pyrefly: ignore [missing-import]

def test_rag_pipeline_initialization():
    pipeline = RAGPipeline()
    assert pipeline.retriever is not None
    assert pipeline.foundry_client is not None

def test_rag_deterministic_fallback_when_no_context():
    """
    FR-14 & NFR-03 (Kritik Fallback Testi):
    Bilgi tabanında yeterli kaynak bulunamayan bir soru sorulduğunda:
    1. has_context False dönmeli
    2. answer FALLBACK_MESSAGE eşit olmalı
    3. sources boş liste [] dönmeli
    4. LLM hiç çağrılmamalıdır.
    """
    pipeline = RAGPipeline()
    unmatched_query = "Mars yüzeyinde hangi gübre kullanılmalıdır?"
    
    with patch.object(pipeline.retriever, 'retrieve', return_value=[]):
        with patch.object(pipeline.foundry_client, 'generate_answer') as mock_llm:
            result = pipeline.answer_question(unmatched_query, use_llm=True)
            
            # LLM'in çağrılmadığını doğrula
            mock_llm.assert_not_called()
            
            # Deterministik yanıt yapısını doğrula
            assert result["has_context"] is False
            assert result["answer"] == FALLBACK_MESSAGE
            assert result["sources"] == []


def test_rag_without_llm_flag():
    pipeline = RAGPipeline()
    query = "Bileşik faiz nedir?"
    result = pipeline.answer_question(query, use_llm=False)
    
    assert isinstance(result, dict)
    assert "answer" in result
    assert "sources" in result
    assert "has_context" in result
    if result["has_context"]:
        assert "[LLM Devre Dışı]" in result["answer"]
        assert len(result["sources"]) > 0

def test_rag_successful_generation_with_mocked_llm():
    pipeline = RAGPipeline()
    query = "Yatırım fonu nasıl çalışır?"
    mock_llm_response = "Yatırım fonları profesyonel yöneticiler tarafından yönetilir."
    
    with patch.object(pipeline.foundry_client, 'generate_answer', return_value=mock_llm_response):
        result = pipeline.answer_question(query, use_llm=True)
        
        if result["has_context"]:
            assert result["answer"] == mock_llm_response
            assert len(result["sources"]) > 0
