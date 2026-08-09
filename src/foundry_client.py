import requests
import json
from src.config import LLM_MODEL, FOUNDRY_BASE_URL  # pyrefly: ignore [missing-import]

class FoundryClient:
    def __init__(self, base_url=FOUNDRY_BASE_URL):
        # Microsoft Foundry Local veya OpenAI uyumlu yerel sunucu adresi
        self.base_url = base_url
        self.model = LLM_MODEL
        
    def is_available(self) -> bool:
        """Sunucunun erişilebilir olup olmadığını kontrol eder."""
        try:
            url = f"{self.base_url.rstrip('/')}/models"
            res = requests.get(url, timeout=3)
            return res.status_code == 200
        except Exception:
            return False

    def generate_answer(self, system_prompt, context, query):
        """
        Retriever'dan gelen bağlamı (context) ve kullanıcı sorusunu (query) kullanarak
        Yerel Foundry / OpenAI uyumlu LLM modelinden cevap üretir (FR-11).
        Bağlantı kurulamazsa None döndürür.
        """
        clean_base = self.base_url.rstrip('/') if self.base_url else ""
        endpoints_to_try = [
            clean_base,
            "http://localhost:8000/v1",
            "http://localhost:11434/v1"  # Ollama OpenAI-compatible endpoint
        ]
        
        seen = set()
        unique_endpoints = [e for e in endpoints_to_try if e and not (e in seen or seen.add(e))]
        
        user_content = f"Aşağıdaki bağlam bilgisini kullanarak soruyu cevapla.\n\nBağlam (Context):\n{context}\n\nSoru: {query}"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.3,
            "max_tokens": 1024
        }
        
        for base in unique_endpoints:
            endpoint = f"{base}/chat/completions"
            try:
                response = requests.post(
                    endpoint, 
                    json=payload, 
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()
                answer = data["choices"][0]["message"]["content"]
                return answer
            except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError):
                continue
                
        print("Foundry Local veya alternatif LLM sunucularına erişilemedi.")
        return None




if __name__ == "__main__":
    # Test amaçlı
    client = FoundryClient()
    print("FoundryClient test ediliyor (Sunucunun çalıştığından emin olun)...")
    
    test_system = "Sen finansal konularda yardımcı olan uzman bir asistansın."
    test_context = "Bileşik faiz, kazanılan faizin anaparaya eklenerek bir sonraki dönemde bu toplam üzerinden tekrar faiz hesaplanmasıdır."
    test_query = "Bileşik faiz kısaca nedir?"
    
    cevap = client.generate_answer(test_system, test_context, test_query)
    print("\nÜretilen Cevap:\n", cevap)
