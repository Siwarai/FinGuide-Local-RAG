import requests
import json
from src.config import LLM_MODEL

class FoundryClient:
    def __init__(self, base_url="http://localhost:8000/v1"):
        # Microsoft Foundry Local veya OpenAI uyumlu yerel sunucu adresi
        self.base_url = base_url
        self.model = LLM_MODEL
        
    def generate_answer(self, system_prompt, context, query):
        """
        Retriever'dan gelen bağlamı (context) ve kullanıcı sorusunu (query) kullanarak
        Yerel Foundry LLM modelinden cevap üretir (FR-11).
        """
        endpoint = f"{self.base_url}/chat/completions"
        
        # Prompt'u bağlam ve soru ile birleştiriyoruz
        user_content = f"Aşağıdaki bağlam bilgisini kullanarak soruyu cevapla.\n\nBağlam (Context):\n{context}\n\nSoru: {query}"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.3, # Daha tutarlı ve deterministik cevaplar için
            "max_tokens": 1024
        }
        
        try:
            response = requests.post(
                endpoint, 
                json=payload, 
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            
            # OpenAI API formatındaki yanıtı parse et
            answer = data["choices"][0]["message"]["content"]
            return answer
            
        except requests.exceptions.RequestException as e:
            print(f"Foundry Local API Bağlantı Hatası: {e}")
            return "Üzgünüm, şu anda yerel model sunucusuna (Foundry) bağlanamadığım için yanıt üretemiyorum."

if __name__ == "__main__":
    # Test amaçlı
    client = FoundryClient()
    print("FoundryClient test ediliyor (Sunucunun çalıştığından emin olun)...")
    
    test_system = "Sen finansal konularda yardımcı olan uzman bir asistansın."
    test_context = "Bileşik faiz, kazanılan faizin anaparaya eklenerek bir sonraki dönemde bu toplam üzerinden tekrar faiz hesaplanmasıdır."
    test_query = "Bileşik faiz kısaca nedir?"
    
    cevap = client.generate_answer(test_system, test_context, test_query)
    print("\nÜretilen Cevap:\n", cevap)
