FinGuide AI — Local Financial Literacy Assistant
FinGuide AI, finansal okuryazarlık alanındaki soruları yerel bilgi tabanından getirilen kaynaklara dayanarak yanıtlamak için tasarlanmış Python tabanlı bir RAG (Retrieval-Augmented Generation) uygulamasıdır.
> **Temel prensip: Yeterli kaynak yoksa model cevap üretmez.**
Kullanıcının sorusu önce bilgi tabanında aranır. İlgili ve yeterli kaynaklar bulunduğunda bu içerikler yerel LLM'e bağlam olarak aktarılır. Kaynaklar yeterli değilse sistem güvenli bir fallback davranışı gösterir.
Projenin Amacı
FinGuide AI'ın amacı, finansal kavramları kullanıcıya anlaşılır biçimde açıklayan ancak cevaplarını mümkün olduğunca belirli bir bilgi tabanına dayandıran yerel bir yapay zekâ asistanı geliştirmektir.
Sistem özellikle şu problemleri azaltmayı hedefler:
Kaynaksız LLM cevapları
Finansal konularda bilgi uydurma (hallucination)
Kullanıcının cevabın hangi içeriklere dayandığını görememesi
Hassas dokümanların gereksiz şekilde bulut servislerine gönderilmesi
Finans alanı dışındaki sorulara kontrolsüz cevap verilmesi
Temel Özellikler
Microsoft Foundry Local ile cihaz üzerinde LLM üretimi
Qwen 3.5 2B Text yerel modeli
`intfloat/multilingual-e5-large` embedding modeli
1024 boyutlu embedding vektörleri
Persistent ChromaDB vector database
Hybrid retrieval
Top-K kaynak getirme
Retrieval skoruna dayalı kaynak yeterlilik kontrolü
Cevapla birlikte kaynak gösterimi
LLM cevap kalite kontrolü
Kaynak-temelli deterministik fallback
Alan dışı sorularda güvenli ret
TXT ve metin katmanlı PDF ingestion
Streamlit web arayüzü
pytest tabanlı test altyapısı
Sistem Mimarisi
```text
Kullanıcı Sorusu
       |
       v
Query Embedding
       |
       v
Hybrid Retrieval
       |
       v
Kaynak Yeterlilik Kontrolü
       |
       +---- Yetersiz ----> Deterministik Fallback
       |
       v
Retrieved Context
       |
       v
Foundry Local / Qwen 3.5 2B
       |
       v
Cevap Kalite Kontrolü
       |
       +---- Başarısız ----> Fallback
       |
       v
Cevap + Kaynaklar + Skorlar
```
Teknoloji Yığını
Teknoloji	Kullanım amacı
Python	Ana geliştirme dili
Microsoft Foundry Local	Yerel LLM çalıştırma
Qwen 3.5 2B Text	Cevap üretimi
Sentence Transformers	Embedding üretimi
multilingual-e5-large	Çok dilli metin embedding'i
ChromaDB	Persistent vector database
Streamlit	Kullanıcı arayüzü
pypdf	PDF metin çıkarımı
pytest	Otomatik testler
Başlangıç Konfigürasyonu
```text
LLM                    qwen3.5-2b-text
Embedding              intfloat/multilingual-e5-large
Embedding dimension    1024
Chunk size             900
Chunk overlap          140
Top K                  4
Minimum retrieval      0.55
Bilgi tabanı           yaklaşık 540 chunk
```
Proje Yapısı
```text
FinGuide-Local-RAG/
│
├── app.py
├── documents/
│   └── finansal bilgi tabanı
│
├── src/
│   ├── config.py
│   ├── embedding.py
│   ├── vector_store.py
│   ├── ingest.py
│   ├── retriever.py
│   ├── foundry_client.py
│   └── rag.py
│
├── tests/
├── docs/
│
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```
Kurulum
1. Repository'yi bilgisayara alın
```powershell
git clone <REPOSITORY_URL>
cd FinGuide-Local-RAG
```
2. Virtual environment oluşturun
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1
```
3. Python paketlerini kurun
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
4. Foundry Local kurulumu
Windows ortamında:
```powershell
winget install Microsoft.FoundryLocal
```
Kontrol:
```powershell
foundry --version
foundry model list
```
Bilgi Tabanını Hazırlama
`documents/` klasörüne TXT veya metin katmanına sahip PDF dosyaları eklenebilir.
İndeksleme:
```powershell
python -m src.ingest
```
Chunk sayısını kontrol etmek için:
```powershell
python -c "from src.vector_store import VectorStore; print(VectorStore().count())"
```
Embedding modeli değiştirildiğinde vector index yeniden oluşturulmalıdır. Generation modelinin değiştirilmesi embedding index'inin yeniden oluşturulmasını gerektirmez.
Retrieval Testi
```powershell
python -m src.retriever "Bileşik faiz nasıl çalışır?"
```
Context'i görmek için:
```powershell
python -m src.retriever "Bileşik faiz nasıl çalışır?" --show-context
```
Foundry Local Testi
```powershell
python -m src.foundry_client "Bileşik faiz nedir?"
```
RAG Testi
```powershell
python -m src.rag "Yatırım fonu nedir?" --use-llm
```
Karşılaştırma örneği:
```powershell
python -m src.rag "Tahvil ile hisse senedi arasındaki fark nedir?" --use-llm
```
Güvenli Ret / Fallback Testi
```powershell
python -m src.rag "Mars'ta tarım yapmak için hangi gübre kullanılmalıdır?" --use-llm
```
Beklenen davranış:
```text
Kaynak bulunamadı / kaynaklar yetersiz
        ↓
LLM çağrısı yapılmaz
        ↓
Güvenli fallback
```
Streamlit
```powershell
streamlit run .\app.py
```
Uygulama akışı:
Kullanıcı sorusu alınır.
Soru embedding'e dönüştürülür.
İlgili kaynaklar aranır.
Kaynak yeterliliği kontrol edilir.
Yeterli kaynak varsa yerel LLM çağrılır.
Cevap kalite kontrolünden geçirilir.
Cevap ve kaynaklar kullanıcıya gösterilir.
Testler
```powershell
python -m pytest
```
Coverage:
```powershell
python -m pytest --cov=src --cov-report=term-missing
```
Gizlilik
FinGuide AI yerel çalışma prensibiyle tasarlanmıştır.
Dokümanlar ChromaDB üzerinde yerel olarak indekslenir.
Cevap üretimi Foundry Local üzerinden cihaz üzerinde gerçekleştirilir.
Kullanıcı dokümanlarının bulut tabanlı bir LLM'e gönderilmesi projenin temel çalışma modeli değildir.
Embedding modeli ilk kurulum sırasında Hugging Face Hub üzerinden indirilebilir.
Model cache'e alındıktan sonra tekrar indirme gerekmeyebilir.
Model Sınırlamaları
Yerel küçük modeller bazı karmaşık sorularda büyük bulut modellerinden daha yavaş veya daha az tutarlı olabilir. Bu nedenle retrieval threshold, kaynak gösterimi, cevap kalite kontrolü ve fallback birlikte kullanılır.
Finansal Sorumluluk Reddi
FinGuide AI finansal eğitim ve genel bilgilendirme amacıyla geliştirilmiştir.
Sistem tarafından verilen cevaplar kişiye özel yatırım, kredi, vergi, hukuk, sigorta veya emeklilik tavsiyesi olarak değerlendirilmemelidir.
Bilinen Sınırlamalar
Bilgi tabanının güncelliği cevap kalitesini etkiler.
Metin katmanı olmayan PDF'ler MVP ingestion akışına uygun değildir.
Embedding modeli değiştirildiğinde index yeniden oluşturulmalıdır.
Yerel LLM performansı donanıma bağlıdır.
Retrieval yanlış kaynak getirirse cevap kalitesi düşebilir.
`0.55` retrieval skoru bir doğruluk yüzdesi değildir; kaynak yeterliliği için kullanılan eşiktir.
Gelecek Sürümleri
Daha geniş ve güncel finansal bilgi tabanı
Gelişmiş hybrid retrieval
Reranker
Daha güçlü local LLM seçenekleri
Gelişmiş cevap değerlendirme
Kullanıcı soru geçmişi
PDF/JSON raporlama
FastAPI backend
React frontend
Docker desteği
MVP Durumu
[x] Local RAG mimarisi
[x] Local LLM yaklaşımı
[x] Embedding + vector database
[x] Retrieval
[x] Kaynak kontrolü
[x] Fallback yaklaşımı
[x] Streamlit arayüzü
[x] TXT/PDF ingestion
[x] Test altyapısı
[ ] Yerel ortamda son doğrulama
[ ] Demo senaryosunun hazırlanması
[ ] GitHub teslim sürümünün son temizliği
Lisans ve Açık Kaynak Kullanımı
Projede kullanılan üçüncü taraf kütüphanelerin, modellerin ve temel alınan açık kaynak kodun lisans koşulları korunmalıdır.
Bu README, referans alınan repository'nin metninin birebir kopyası değildir; aynı teknik gerçekleri koruyarak proje teslimi için yeniden düzenlenmiştir.
Kaynak
Temel teknik referans olarak FinGuide-Local-RAG repository'sindeki README, proje yapısı, kurulum, ingestion, retrieval, Foundry Local, RAG, Streamlit, test, gizlilik ve lisans bölümleri incelenmiştir.