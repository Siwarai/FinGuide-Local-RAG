<div align="center">

# 📈 FinGuide AI
### *Local Financial Literacy Assistant & RAG Engine*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-purple?style=for-the-badge)
![Microsoft Foundry](https://img.shields.io/badge/Microsoft-Foundry_Local-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<p align="center">
  <b>Cihaz üzerinde çalışan, gizlilik odaklı, doğrulanabilir kaynak gösterimli finansal RAG asistanı.</b><br>
  <i>"Yeterli kaynak yoksa model uydurmaz, güvenli ret (fallback) mekanizmasını çalıştırır."</i>
</p>

[📌 Amaç](#-projenin-amacı) •
[🌟 Özellikler](#-temel-özellikler) •
[🏗️ Mimari](#%EF%B8%8F-sistem-mimarisi) •
[🚀 Kurulum](#-kurulum) •
[🖥️ Web Arayüzü](#%EF%B8%8F-streamlit-web-arayüzü) •
[📊 MVP Durumu](#-mvp-durumu)

---

</div>

> [!IMPORTANT]
> **Güvenilir Finansal Asistan İlkesi:**  
> Kullanıcının sorusu önce yerel bilgi tabanında taranır. Yeterli benzerlik eşiğini (`0.55`) aşan doğrulanabilir kaynaklar bulunduğunda yerel LLM'e bağlam aktarılır. Kaynaklar yetersiz ise sistem uydurma bilgi üretmemek için **deterministik fallback** yanıtını döndürür.

---

## 🎯 Projenin Amacı

**FinGuide AI**, finansal okuryazarlık alanındaki soruları kullanıcıya anlaşılır biçimde açıklayan, fakat tüm yanıtlarını **doğrudan yerel doküman bilgi tabanına dayandıran** bir RAG (*Retrieval-Augmented Generation*) mimarisidir.

### 🛡️ Çözülen Temel Problemler

| Problem | FinGuide AI Çözümü |
| :--- | :--- |
| **Kaynaksız LLM Yanıtları** | Üretilen her yanıtın altına kaynak doküman adı ve benzerlik skoru eklenir. |
| **Bilgi Uydurma (*Hallucination*)** | Yetersiz kaynak durumunda LLM hiç çağrılmaz, sabit ve güvenli fallback yanıtı dönülür. |
| **Bulut Veri Gizliliği Riski** | Tüm arama ve cevap üretimi **%100 yerelde (cihaz üzerinde)** gerçekleştirilir. |
| **Finans Dışı Sorular** | Bilgi tabanında bulunmayan finans dışı konular otomatik olarak reddedilir. |

---

## 🌟 Temel Özellikler

<table>
  <tr>
    <td width="50%">
      <h3>🔒 %100 Yerel Mimarisi</h3>
      <ul>
        <li><b>Microsoft Foundry Local:</b> Cihaz üzerinde Qwen 3.5 2B Text yerel LLM çalıştırması.</li>
        <li><b>Yerel Vektör Veritabanı:</b> ChromaDB ile persistent vektör indeksleme.</li>
        <li><b>Gizlilik Garantisi:</b> Dokümanlar ve sorular asla dış sunuculara gönderilmez.</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🧠 Akıllı Retrieval & Kontrol</h3>
      <ul>
        <li><b>Multilingual Embedding:</b> 1024 boyutlu <code>multilingual-e5-large</code> vektörleri.</li>
        <li><b>Skora Dayalı Filtreleme:</b> Retrieval skoru eşiği (Min: <code>0.55</code>).</li>
        <li><b>Cevap Kalite Kontrolü:</b> LLM çıktısının doğrulanması ve şeffaf kaynak gösterimi.</li>
      </ul>
    </td>
  </tr>
</table>

---

## 🏗️ Sistem Mimarisi

```mermaid
flowchart TD
    A[💬 Kullanıcı Sorusu] --> B[🔍 Query Embedding]
    B --> C[📚 ChromaDB Vector Store]
    C --> D{⚖️ Kaynak Yeterlilik Kontrolü<br/>Score >= 0.55}
    
    D -- ❌ Yetersiz Kaynak --v E[🛡️ Deterministik Fallback Yanıtı]
    D -- ✅ Yeterli Kaynak --> F[📝 Bağlam / Context Birleştirme]
    
    F --> G[🤖 Foundry Local - Qwen 3.5 2B]
    G --> H{🧪 Cevap Kalite Kontrolü}
    
    H -- ❌ Başarısız --> E
    H -- ✅ Başarılı --> I[📊 Cevap + Kaynak Listesi + Skorlar]

    style A fill:#2d3748,color:#fff,stroke:#4a5568
    style D fill:#d69e2e,color:#fff,stroke:#b7791f
    style E fill:#e53e3e,color:#fff,stroke:#c53030
    style I fill:#38a169,color:#fff,stroke:#2f855a
```

---

## 🛠️ Teknoloji Yığını

```text
               ┌─────────────────────────────────────────┐
               │        Streamlit Web Interface          │
               └────────────────────┬────────────────────┘
                                    │
               ┌────────────────────▼────────────────────┐
               │         RAG Pipeline (src/rag.py)       │
               └──────┬───────────────────────────┬──────┘
                      │                           │
  ┌───────────────────▼───────────┐   ┌───────────▼──────────────────┐
  │     Embedding & Retriever     │   │   LLM Generation Engine      │
  │   - Sentence Transformers     │   │   - Microsoft Foundry Local  │
  │   - multilingual-e5-large     │   │   - Qwen 3.5 2B Text         │
  │   - ChromaDB (Persistent)     │   └──────────────────────────────┘
  └───────────────────────────────┘
```

---

## ⚙️ Başlangıç Konfigürasyonu

| Konfigürasyon | Değer | Açıklama |
| :--- | :--- | :--- |
| **LLM Modeli** | `qwen3.5-2b-text` | Microsoft Foundry Local yerel dil modeli |
| **Embedding Modeli** | `intfloat/multilingual-e5-large` | Çok dilli vektörleştirme modeli |
| **Embedding Vektör Boyutu** | `1024` | Vektör uzayı boyutu |
| **Chunk Boyutu (Chunk Size)** | `900` karakter | Metin parçalama boyutu |
| **Örtüşme (Chunk Overlap)** | `140` karakter | Parçalar arası metin örtüşmesi |
| **Getirilecek Kaynak (Top-K)** | `4` | Vektör aramada getirilen maks. parça |
| **Min. Retrieval Skoru** | `0.55` | Kaynak yeterlilik eşik skoru |

---

## 📁 Proje Yapısı

```text
FinGuide-Local-RAG/
│
├── 📄 app.py                   # Streamlit web arayüzü uygulaması
├── 📂 documents/               # Finansal doküman bilgi tabanı (.txt, .pdf)
│   └── 📄 finansal_rehber.txt  # Örnek finansal test rehberi
│
├── 📂 src/                     # Çekirdek Python modülleri
│   ├── ⚙️ config.py            # Konfigürasyon ve parametre ayarları
│   ├── 🧬 embedding.py         # Metin vektörleştirme (SentenceTransformers)
│   ├── 💾 vector_store.py      # ChromaDB vektör veri tabanı yönetimi
│   ├── ✂️ ingest.py            # Doküman okuma, chunking ve indeksleme
│   ├── 🔎 retriever.py         # Vektörel arama ve benzerlik skorlama
│   ├── 🔌 foundry_client.py    # Foundry Local LLM API istemcisi
│   └── 🔄 rag.py               # Uçtan uca RAG Pipeline mantığı
│
├── 📂 tests/                   # Otomatik pytest birim testleri
├── 📂 docs/                    # Mimari ve gereksinim dokümanları
│
├── 📄 requirements.txt         # Python bağımlılık listesi
├── 📄 pyproject.toml           # Proje araç yapılandırmaları
├── 📄 .env.example             # Örnek ortam değişkenleri
└── 📄 README.md                # Proje dokümantasyonu
```

---

## 🚀 Kurulum ve Çalıştırma

<details>
<summary><b>1. Repository'yi Klonlama ve Ortam Kurulumu (Tıklayın)</b></summary>

```powershell
# 1. Projeyi klonlayın
git clone https://github.com/Siwarai/FinGuide-Local-RAG.git
cd FinGuide-Local-RAG

# 2. Sanal ortamı (venv) oluşturun ve aktifleştirin
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1

# 3. Bağımlılıkları yükleyin
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
</details>

<details>
<summary><b>2. Microsoft Foundry Local Kurulumu (Tıklayın)</b></summary>

```powershell
# Windows ortamında Foundry Local kurulumu
winget install Microsoft.FoundryLocal

# Kurulum kontrolü
foundry --version
foundry model list
```
</details>

<details>
<summary><b>3. Doküman İndeksleme ve CLI Testleri (Tıklayın)</b></summary>

```powershell
# 1. documents/ klasöründeki metinleri indeksleyin
python -m src.ingest

# 2. Retrieval testini çalıştırın
python -m src.retriever "Bileşik faiz nasıl çalışır?" --show-context

# 3. Uçtan uca RAG pipeline testini çalıştırın
python -m src.rag "Yatırım fonu nedir?" --use-llm

# 4. Güvenli Ret (Fallback) testini çalıştırın
python -m src.rag "Mars'ta tarım nasıl yapılır?" --use-llm
```
</details>

---

## 🖥️ Streamlit Web Arayüzü

Arayüzü başlatmak için aşağıdaki komutu çalıştırın:

```powershell
streamlit run app.py
```

> [!TIP]
> **Streamlit Özellikleri:**
> - 🎯 **Özel Filtreler:** Yan menüden yerel LLM kullanımını açıp kapatma imkanı.
> - 📊 **Benzerlik Yüzdesi:** Yanıtla birlikte kullanılan tüm kaynakların benzerlik skorları (`%XX.XX`) görünür.
> - ⚠️ **Gelişmiş Fallback Görünümü:** Yetersiz kaynak durumunda belirgin arayüz uyarısı.
> - 📜 **Yasal Sorumluluk Reddi:** Her sayfanın altında otomatik finansal uyarı beyanı.

---

## 🔍 Testler ve Test Kapsaması

Test suite'ini çalıştırmak için:

```powershell
# Pytest ile birim testlerini çalıştırın
python -m pytest

# Test kapsama (coverage) raporu alın
python -m pytest --cov=src --cov-report=term-missing
```

---

## ⚠️ Finansal Sorumluluk Reddi (Disclaimer)

> [!CAUTION]
> **Yasal Uyarı:**  
> FinGuide AI tarafından sunulan yanıtlar, veriler ve analizler yalnızca **genel bilgilendirme ve eğitim** amacıyla üretilmektedir. Burada yer alan hiçbir bilgi kişiye özel yatırım danışmanlığı, finansal tavsiye veya alım-satım önerisi niteliği taşımaz.

---

## 📊 MVP Durumu

- [x] **Local RAG Mimarisi** (ChromaDB + SentenceTransformers)
- [x] **Local LLM Entegrasyonu** (Microsoft Foundry Local / Qwen 3.5 2B)
- [x] **Skora Dayalı Ret (Fallback)** (Min Retrieval Score: `0.55`)
- [x] **Streamlit Kullanıcı Arayüzü** (Dinamik kaynak ve skor kartları)
- [x] **TXT ve PDF Ingestion**
- [x] **Pytest Test Altyapısı**
- [x] **Doğrulanmış Yerel Test Senaryoları**

---

<div align="center">

  <b>FinGuide AI</b> • Developed with ❤️ for Local & Secure AI Solutions

</div>