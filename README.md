# 📈 FinGuide AI — Local Financial Literacy Assistant

**FinGuide AI**, finansal okuryazarlık alanındaki soruları yerel bilgi tabanından getirilen kaynaklara dayanarak yanıtlamak için tasarlanmış Python tabanlı bir **RAG (Retrieval-Augmented Generation)** uygulamasıdır.

> ⚠️ **Temel Prensip:** Yeterli kaynak yoksa model cevap üretmez!  
> Kullanıcının sorusu önce bilgi tabanında aranır. İlgili ve yeterli kaynaklar bulunduğunda bu içerikler yerel LLM'e bağlam olarak aktarılır. Kaynaklar yeterli değilse sistem güvenli bir **deterministik fallback** davranışı gösterir.

---

## 🎯 Projenin Amacı

FinGuide AI'ın amacı, finansal kavramları kullanıcıya anlaşılır biçimde açıklayan ancak cevaplarını mümkün olduğunca belirli bir bilgi tabanına dayandıran yerel bir yapay zekâ asistanı geliştirmektir.

Sistem özellikle şu problemleri ortadan kaldırmayı hedefler:
- ❌ Kaynaksız ve dayanağı olmayan LLM cevapları
- ❌ Finansal konularda bilgi uydurma (*hallucination*)
- ❌ Kullanıcının cevabın hangi kaynaklara dayandığını görememesi
- ❌ Hassas dokümanların bulut servislerine gönderilmesi riskleri
- ❌ Finans alanı dışındaki sorulara kontrolsüz cevap verilmesi

---

## 🌟 Temel Özellikler

- **Yerel LLM Üretimi:** Microsoft Foundry Local ile cihaz üzerinde çalıştırma (Qwen 3.5 2B Text).
- **Vektör Temsili (Embedding):** `intfloat/multilingual-e5-large` modeli ile 1024 boyutlu vektörler.
- **Vektör Veri Tabanı:** Persistent ChromaDB entegrasyonu.
- **Gelişmiş Retrieval:** Hybrid retrieval, Top-K kaynak getirme ve skora dayalı filtreleme.
- **Kaynak Yeterlilik Kontrolü:** Belirlenen benzerlik eşiğinin (`0.55`) altındaki durumlarda **güvenli ret (fallback)**.
- **Şeffaf Kaynak Gösterimi:** Üretilen her yanıtla birlikte kullanılan metin parçaları (chunk) ve benzerlik skorları sunulur.
- **Çoklu Format Desteği:** TXT ve metin katmanlı PDF ingestion yeteneği.
- **Kullanıcı Arayüzü:** Streamlit tabanlı modern ve dinamik web arayüzü.
- **Test Altyapısı:** `pytest` ve `pytest-cov` tabanlı birim/entegrasyon test altyapısı.

---

## 🏗️ Sistem Mimarisi

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
        +-------------+-------------+
        |                           |
    Yetersiz                     Yeterli
        |                           |
        v                           v
  Deterministik             Retrieved Context
    Fallback                        |
                                    v
                       Foundry Local / Qwen 3.5 2B
                                    |
                                    v
                          Cevap Kalite Kontrolü
                                    |
                    +---------------+---------------+
                    |                               |
                Başarısız                        Başarılı
                    |                               |
                    v                               v
                Fallback                   Cevap + Kaynaklar + Skorlar
```

---

## 🛠️ Teknoloji Yığını

| Teknoloji | Kullanım Amacı |
| :--- | :--- |
| **Python** | Ana geliştirme dili |
| **Microsoft Foundry Local** | Yerel LLM çalıştırma ortamı |
| **Qwen 3.5 2B Text** | Cevap üretimi yapan yerel dil modeli |
| **Sentence Transformers** | Embedding üretimi kütüphanesi |
| **multilingual-e5-large** | Çok dilli metin embedding modeli |
| **ChromaDB** | Kalıcı (Persistent) Vektör Veri Tabanı |
| **Streamlit** | Kullanıcı arayüzü (UI) |
| **pypdf** | PDF metin çıkarımı kütüphanesi |
| **pytest** | Otomatik test ve kapsama altyapısı |

---

## ⚙️ Başlangıç Konfigürasyonu

| Parametre | Değer | Açıklama |
| :--- | :--- | :--- |
| **LLM Model** | `qwen3.5-2b-text` | Yerel LLM modeli |
| **Embedding Model** | `intfloat/multilingual-e5-large` | Metin vektörleştirme modeli |
| **Embedding Boyutu** | `1024` | Vektör uzayı boyutu |
| **Chunk Size** | `900` | Metin parçalama boyutu (karakter) |
| **Chunk Overlap** | `140` | Parça örtüşme boyutu (karakter) |
| **Top K** | `4` | Getirilecek maksimum kaynak sayısı |
| **Minimum Retrieval Score**| `0.55` | Kaynak yeterlilik skoru eşiği |

---

## 📁 Proje Yapısı

```text
FinGuide-Local-RAG/
│
├── app.py                      # Streamlit kullanıcı arayüzü
├── documents/                  # Finansal bilgi tabanı dokümanları (.txt, .pdf)
│
├── src/                        # Kaynak kodlar
│   ├── config.py               # Sistem konfigürasyon ayarları
│   ├── embedding.py            # SentenceTransformer entegrasyonu
│   ├── vector_store.py         # ChromaDB vektör veri tabanı yönetimi
│   ├── ingest.py               # Doküman okuma ve parçalama (chunking)
│   ├── retriever.py            # Vektörel arama ve filtreleme
│   ├── foundry_client.py       # Foundry Local LLM istemcisi
│   └── rag.py                  # Uçtan uca RAG boru hattı (Pipeline)
│
├── tests/                      # Birim ve entegrasyon testleri
├── docs/                       # Proje dokümantasyonu
│
├── requirements.txt            # Python bağımlılıkları
├── pyproject.toml              # Proje araç konfigürasyonları
├── .env.example                # Örnek ortam değişkenleri
├── .gitignore                  # Git yoksayma kuralları
├── LICENSE                     # Lisans dosyası
└── README.md                   # Proje tanıtım dosyası
```

---

## 🚀 Kurulum

### 1. Repository'yi Klonlayın
```powershell
git clone https://github.com/Siwarai/FinGuide-Local-RAG.git
cd FinGuide-Local-RAG
```

### 2. Sanal Ortam (Virtual Environment) Oluşturun ve Aktifleştirin
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1
```

### 3. Bağımlılıkları Yükleyin
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Microsoft Foundry Local Kurulumu
Windows ortamında Foundry Local uygulamasını kurun:
```powershell
winget install Microsoft.FoundryLocal
```

Kurulumu doğrulayın:
```powershell
foundry --version
foundry model list
```

---

## 📚 Bilgi Tabanını Hazırlama (Ingestion)

`documents/` klasörüne finansal `.txt` veya metin katmanına sahip `.pdf` dosyalarınızı ekleyin.

**Dokümanları Vektör Veri Tabanına İndeksleme:**
```powershell
python -m src.ingest
```

**İndekslenen Chunk Sayısını Kontrol Etme:**
```powershell
python -c "from src.vector_store import VectorStore; print(f'Toplam Chunk Sayısı: {VectorStore().count()}')"
```

> 📌 **Not:** Embedding modeli değiştirildiğinde vektör indeksi yeniden oluşturulmalıdır. LLM (generation) modelinin değiştirilmesi vektör indeksini etkilemez.

---

## 🧪 Test ve Çalıştırma

### 🔍 1. Retrieval (Arama) Testi
```powershell
python -m src.retriever "Bileşik faiz nasıl çalışır?"
```
*Bağlam metinlerini (chunk içeriğini) de görmek için:*
```powershell
python -m src.retriever "Bileşik faiz nasıl çalışır?" --show-context
```

### 🤖 2. Foundry Local (LLM) Testi
```powershell
python -m src.foundry_client "Bileşik faiz nedir?"
```

### ⚡ 3. RAG Pipeline Testi
```powershell
python -m src.rag "Yatırım fonu nedir?" --use-llm
```

### 🛡️ 4. Güvenli Ret / Fallback Testi
```powershell
python -m src.rag "Mars'ta tarım yapmak için hangi gübre kullanılmalıdır?" --use-llm
```
*Beklenen Davranış:*
```text
Kaynak bulunamadı / kaynaklar yetersiz
        ↓
LLM çağrısı yapılmaz
        ↓
Güvenli Fallback Yanıtı Döndürülür
```

---

## 🖥️ Streamlit Web Arayüzü

Arayüzü başlatmak için:
```powershell
streamlit run app.py
```

### 🔄 Uygulama Akışı:
1. Kullanıcıdan finansal soru alınır.
2. Soru vektörleştirilir (Query Embedding).
3. ChromaDB üzerinde ilgili kaynaklar aranır (Retrieval).
4. Benzerlik skorlarına göre kaynak yeterliliği denetlenir (`>= 0.55`).
5. Yeterli kaynak varsa yerel LLM (Foundry Local) çağrılarak yanıt üretilir.
6. Yanıt, kullanılan kaynaklar, benzerlik skorları ve yasal sorumluluk reddi uyarısı ile birlikte kullanıcıya gösterilir.

---

## 🔍 Testler ve Kapsama (Coverage)

Otomatik testleri çalıştırmak için:
```powershell
python -m pytest
```

Test kapsama raporu almak için:
```powershell
python -m pytest --cov=src --cov-report=term-missing
```

---

## 🔒 Gizlilik ve Güvenlik

- **%100 Yerel Çalışma:** FinGuide AI yerel çalışma prensibiyle tasarlanmıştır.
- **Veri Gizliliği:** Dokümanlar ChromaDB üzerinde yerel olarak indekslenir, tüm sorgular ve LLM yanıtları cihaz üzerinde işlenir. Bulut servislerine veri aktarılmaz.
- **Model Önbelleği:** Embedding modeli ilk kurulumda Hugging Face Hub üzerinden indirilir ve yerel önbelleğe alınır.

---

## ⚠️ Finansal Sorumluluk Reddi Beyanı (Disclaimer)

FinGuide AI, yalnızca finansal okuryazarlık, eğitim ve genel bilgilendirme amacıyla geliştirilmiştir. Sistem tarafından üretilen yanıtlar hiçbir koşulda kişiye özel yatırım, kredi, vergi, hukuk veya finansal danışmanlık tavsiyesi olarak değerlendirilemez.

---

## 📌 Bilinen Sınırlamalar

- Bilgi tabanının güncelliği ve kalitesi doğrudan cevap kalitesini belirler.
- Metin katmanı bulunmayan taranmış (image-based) PDF'ler MVP sürümünde desteklenmemektedir.
- Yerel LLM performansı ve yanıt süresi kullanılan donanıma (CPU/GPU/RAM) bağlıdır.
- `0.55` retrieval skoru bir doğruluk yüzdesi değil, kaynak yeterliliğini belirleyen vektörel kosinüs/mesafe eşiğidir.

---

## 🚀 Gelecek Sürümler (Roadmap)

- [ ] Gelişmiş Hybrid Retrieval ve Reranker entegrasyonu
- [ ] Daha güçlü yerel LLM modelleri için çoklu model desteği
- [ ] Kullanıcı soru geçmişi ve sohbet oturumu (Chat Session) yönetimi
- [ ] PDF/JSON formatında analiz raporlama çıktısı alma
- [ ] FastAPI backend & React tabanlı modern frontend mimarisi
- [ ] Docker konteynerizasyon desteği

---

## 📊 MVP Durumu

- [x] Local RAG mimarisi
- [x] Local LLM yaklaşımı (Foundry Local)
- [x] Embedding + ChromaDB Vektör Veri Tabanı
- [x] Skora dayalı kaynak yeterlilik kontrolü
- [x] Deterministik Fallback mekanizması
- [x] Streamlit web arayüzü
- [x] TXT ve PDF ingestion altyapısı
- [x] Pytest test altyapısı
- [x] Yerel ortamda tam doğrulama

---

## 📜 Lisans ve Açık Kaynak Kullanımı

Projede kullanılan üçüncü taraf kütüphanelerin, modellerin ve temel alınan açık kaynak kod bileşenlerinin lisans koşulları korunmaktadır.