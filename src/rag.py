import argparse
from src.retriever import Retriever
from src.foundry_client import FoundryClient

# FR-14 & NFR-03: Deterministik güvenli fallback mesajı
FALLBACK_MESSAGE = "Üzgünüm, bilgi tabanımda bu soruya yanıt verecek yeterli finansal kaynak bulamadım."

SYSTEM_PROMPT = """Sen FinGuide adında uzman bir finansal asistansın.
Görevin, yalnızca sana verilen bağlam (context) bilgilerini kullanarak kullanıcının finansal sorularını doğru, net ve anlaşılır bir şekilde cevaplamaktır.
Sana verilen bağlam içerisinde cevabı bulunmayan sorular için uydurma bilgiler üretme, sadece verilen kaynaklara sadık kal."""

class RAGPipeline:
    def __init__(self, base_url="http://localhost:8000/v1"):
        self.retriever = Retriever()
        self.foundry_client = FoundryClient(base_url=base_url)
        
    def answer_question(self, query: str, use_llm: bool = True) -> dict:
        """
        Kullanıcı sorusunu alır, veritabanından ilgili metinleri çeker ve LLM ile yanıt üretir.
        """
        # 1. Retriever ile ilgili sonuçları getir
        retrieved_results = self.retriever.retrieve(query)
        
        # FR-14 & NFR-03 (Kritik Fallback): Eğer yeterli kaynak bulunamadıysa LLM'i ÇAĞIRMA
        if not retrieved_results:
            return {
                "answer": FALLBACK_MESSAGE,
                "sources": [],
                "has_context": False
            }
            
        # FR-12: Kullanılan kaynakların ve skorların hazırlanması
        sources_info = [
            {
                "source": res["metadata"].get("source", "Bilinmeyen Kaynak"),
                "score": res["score"],
                "chunk": res["chunk"]
            }
            for res in retrieved_results
        ]
        
        # FR-10: Metinlerin (chunk'ların) bağlam olarak birleştirilmesi
        context_text = "\n\n---\n\n".join([res["chunk"] for res in retrieved_results])
        
        # Eğer LLM kullanımı kapalıysa (sadece test/retrieval kontrolü için)
        if not use_llm:
            return {
                "answer": f"[LLM Devre Dışı] Bulunan Bağlam:\n{context_text}",
                "sources": sources_info,
                "has_context": True
            }
            
        # 2. FoundryClient ile LLM yanıtı üret
        answer = self.foundry_client.generate_answer(
            system_prompt=SYSTEM_PROMPT,
            context=context_text,
            query=query
        )
        
        # FR-12: Bütünleşik sözlük çıktısı
        return {
            "answer": answer,
            "sources": sources_info,
            "has_context": True
        }

if __name__ == "__main__":
    # FR-17: CLI Test Desteği
    parser = argparse.ArgumentParser(description="FinGuide RAG Pipeline CLI Test Aracı")
    parser.add_argument("query", type=str, help="Sorulacak finansal soru")
    parser.add_argument("--use-llm", action="store_true", help="Yerel LLM modelini çağırarak gerçek yanıt üretir")
    
    args = parser.parse_args()
    
    pipeline = RAGPipeline()
    print(f"Soru işleniyor: '{args.query}'...\n")
    
    result = pipeline.answer_question(args.query, use_llm=args.use_llm)
    
    print("=" * 60)
    print("CEVAP:")
    print(result["answer"])
    print("=" * 60)
    
    if result["sources"]:
        print("\nKULLANILAN KAYNAKLAR VE SKORLAR:")
        for idx, src in enumerate(result["sources"], 1):
            print(f"[{idx}] Kaynak Dosya: {src['source']} | Benzerlik Skoru: {src['score']:.4f}")
    else:
        print("\nHiçbir yeterli kaynak bulunamadı (Deterministic Fallback Tetiklendi).")
