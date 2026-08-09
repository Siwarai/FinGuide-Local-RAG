import argparse
from src.config import TOP_K, MIN_RETRIEVAL_SCORE  # pyrefly: ignore [missing-import]
from src.embedding import Embedder  # pyrefly: ignore [missing-import]
from src.vector_store import VectorStore  # pyrefly: ignore [missing-import]

class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        
    def retrieve(self, query, top_k=TOP_K, min_score=MIN_RETRIEVAL_SCORE):
        # 1. Sorguyu vektörelleştir
        query_embedding = self.embedder.embed_query(query)
        
        # 2. Vektör veritabanında ara
        results = self.vector_store.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        if not results or not results.get('documents') or not results['documents'][0]:
            return []
            
        retrieved_chunks = results['documents'][0]
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]
        
        filtered_results = []
        for doc, dist, meta in zip(retrieved_chunks, distances, metadatas):
            # ChromaDB mesafe (distance) döndürür. Benzerlik skoruna çeviriyoruz.
            # (Eğer model/vektör normalize ise veya Cosine kullanılıyorsa, skor 1'e ne kadar yakınsa o kadar benzerdir)
            score = 1.0 / (1.0 + dist)  # Mesafeyi (distance) 0-1 arası bir skora dönüştürmek için basit bir formül
            
            # FR-09: Belirlenen eşiğin altında kalan skorları filtrele
            if score >= min_score:
                filtered_results.append({
                    "chunk": doc,
                    "metadata": meta,
                    "score": score
                })
        
        # Skorlara göre büyükten küçüğe sırala
        filtered_results = sorted(filtered_results, key=lambda x: x["score"], reverse=True)
        return filtered_results

if __name__ == "__main__":
    # FR-16: CLI Test Desteği
    parser = argparse.ArgumentParser(description="Retriever CLI Test Aracı")
    parser.add_argument("query", type=str, help="Arama yapılacak kullanıcı sorgusu")
    parser.add_argument("--show-context", action="store_true", help="Bulunan metin (chunk) içeriklerini de gösterir")
    
    args = parser.parse_args()
    
    retriever = Retriever()
    print(f"'{args.query}' için veritabanında aranıyor...\n")
    
    results = retriever.retrieve(args.query)
    
    if not results:
        print(f"Eşleşen sonuç bulunamadı (Min Score eşiği ({MIN_RETRIEVAL_SCORE}) aşılamadı).")
    else:
        print(f"Toplam {len(results)} alakalı sonuç bulundu:\n")
        for i, res in enumerate(results, 1):
            source = res['metadata'].get('source', 'Bilinmiyor')
            score = res['score']
            print(f"[{i}] Kaynak: {source} | Benzerlik Skoru: {score:.4f}")
            
            if args.show_context:
                print(f"    Metin: {res['chunk']}\n")
                print("-" * 60)
