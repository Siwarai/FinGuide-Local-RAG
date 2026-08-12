import argparse
from src.retriever import Retriever  # pyrefly: ignore [missing-import]
from src.foundry_client import FoundryClient  # pyrefly: ignore [missing-import]
from src.youtube_recommender import YouTubeRecommender  # pyrefly: ignore [missing-import]
from src.config import FOUNDRY_BASE_URL  # pyrefly: ignore [missing-import]

# FR-14 & NFR-03: Deterministik güvenli fallback mesajı
FALLBACK_MESSAGE = "Üzgünüm, bilgi tabanımda bu soruya yanıt verecek yeterli finansal kaynak bulamadım."

SYSTEM_PROMPT = """Sen FinGuide AI adında profesyonel, uzman bir finansal asistansın.
Görevin, sana verilen bağlam (context) bilgilerini inceleyerek kullanıcının sorusunu son derece detaylı, anlaşılır, yapılı ve profesyonel bir şekilde cevaplamaktır.

Yanıtını verirken mümkün olduğunca şu yapıyı kullan:
1. 📌 **Temel Tanım & Özet:** Konunun kısa ve anlaşılır tanımı.
2. 🔍 **Detaylı Açıklama & İşleyiş:** Konunun alt detayları, nasıl çalıştığı ve mekanizması.
3. 💡 **Önemli Kavramlar & Metrikler:** İlgili kritik finansal terimler veya formüller (varsa).
4. 📊 **Pratik Senaryo / Örnek:** Konuyu netleştirecek kısa bir finansal uygulama örneği.
5. ⚠️ **Dikkat Edilmesi Gerekenler & Riskler:** Kullanıcının bilmesi gereken riskler veya tavsiyeler.

Sana verilen bağlam içerisinde cevabı bulunmayan konular için uydurma bilgi üretme, sadece verilen kaynak metinlerine sadık kal."""

class RAGPipeline:
    def __init__(self, base_url=FOUNDRY_BASE_URL):
        self.retriever = Retriever()
        self.foundry_client = FoundryClient(base_url=base_url)
        
    def answer_question(self, query: str, use_llm: bool = True) -> dict:
        """
        Kullanıcı sorusunu alır, veritabanından ilgili metinleri çeker, LLM ile zengin yanıt üretir
        ve ilgili YouTube eğitici videolarını önerir.
        """
        # 1. Retriever ile ilgili sonuçları getir
        retrieved_results = self.retriever.retrieve(query)
        
        # YouTube video önerilerini sorgu bazlı getir
        youtube_videos = YouTubeRecommender.get_recommendations(query)
        
        # FR-14 & NFR-03 (Kritik Fallback): Eğer yeterli kaynak bulunamadıysa LLM'i ÇAĞIRMA
        if not retrieved_results:
            return {
                "answer": FALLBACK_MESSAGE,
                "sources": [],
                "has_context": False,
                "youtube_videos": []
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
                "has_context": True,
                "youtube_videos": youtube_videos
            }
            
        # 2. FoundryClient ile LLM yanıtı üret
        answer = self.foundry_client.generate_answer(
            system_prompt=SYSTEM_PROMPT,
            context=context_text,
            query=query
        )
        
        # Eğer yerel LLM sunucusu çevrimdışı ise, retriever verilerini kullanarak Akıllı Bağlam Yanıtı oluştur (Graceful Fallback)
        if answer is None:
            answer = self._generate_smart_extraction(retrieved_results, query)
        
        # FR-12: Bütünleşik sözlük çıktısı
        return {
            "answer": answer,
            "sources": sources_info,
            "has_context": True,
            "youtube_videos": youtube_videos
        }

    def _generate_smart_extraction(self, retrieved_results: list, query: str) -> str:
        """
        Yerel LLM sunucusu çevrimdışı olduğunda, bulunan en alakalı kaynak parçalarını (chunk)
        süzerek şablon tabanlı akıllı ve anlamlı bir detaylı yanıt (Graceful Fallback / Smart Extraction) oluşturur.
        """
        top_result = retrieved_results[0]
        top_chunk = top_result["chunk"].strip()
        top_source = top_result["metadata"].get("source", "Finansal Bilgi Tabanı Dokümanı")
        top_score = top_result["score"] * 100

        all_chunks = "\n\n".join([f"• {r['chunk'].strip()}" for r in retrieved_results[:3]])

        formatted_answer = (
            f"### 📌 **Temel Finansal Bilgi Tabanı Yanıtı** *(Akıllı Bağlam Süzgeci)*\n\n"
            f"{top_chunk}\n\n"
            f"### 🔍 **Öne Çıkan İlgili Doküman Detayları**\n"
            f"{all_chunks}\n\n"
            f"---\n"
            f"*💡 **Not:** Yerel LLM bağlantısı çevrimdışı olduğu için bu içerik, `{top_source}` dokümanından "
            f"**%{top_score:.1f}** maksimum benzerlik skoru ile doğrudan süzülerek sunulmuştur.*"
        )
        return formatted_answer



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
    
    if result.get("youtube_videos"):
        print("\nÖNERİLEN YOUTUBE VİDEOLARI:")
        for vid in result["youtube_videos"]:
            print(f"🎥 {vid['title']} - {vid['embed_url']}")
    else:
        print("\nHiçbir yeterli kaynak bulunamadı (Deterministic Fallback Tetiklendi).")

