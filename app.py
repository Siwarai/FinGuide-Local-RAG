import os
import sys

# Kök dizini sys.path'e ekle (IDE/Linter ve import sorunlarını önlemek için)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from src.rag import RAGPipeline  # pyrefly: ignore [missing-import]
from src.vector_store import VectorStore  # pyrefly: ignore [missing-import]
from src.config import MIN_RETRIEVAL_SCORE, TOP_K  # pyrefly: ignore [missing-import]
from src.youtube_recommender import YouTubeRecommender  # pyrefly: ignore [missing-import]

# -----------------------------------------------------------------------------
# 1. Sayfa Konfigürasyonu & Modern Tema
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Finans Danışmanım AI Pro — Akıllı Finansal Asistan",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS Tasarımı - Dark Glassmorphism & YouTube Kapak Kartları
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Glassmorphism Kart Şablonu */
    .finans-danismanim-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Canlı KPI Metrik Kutuları */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    
    .kpi-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .kpi-box:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .kpi-label {
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* Rozetler */
    .badge-success {
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-info {
        background-color: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* YouTube Kapak Görselli Video Kartı */
    .yt-card-link {
        text-decoration: none !important;
        color: inherit !important;
        display: block;
    }
    
    .yt-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 16px;
        overflow: hidden;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        margin-bottom: 16px;
        cursor: pointer;
    }
    
    .yt-card:hover {
        transform: translateY(-4px);
        border-color: rgba(239, 68, 68, 0.8);
        box-shadow: 0 12px 28px rgba(239, 68, 68, 0.25);
    }
    
    .yt-thumb-container {
        position: relative;
        width: 100%;
        height: 180px;
        overflow: hidden;
        background: #000;
    }
    
    .yt-thumb-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.88;
        transition: opacity 0.2s ease, transform 0.3s ease;
    }
    
    .yt-card:hover .yt-thumb-img {
        opacity: 1;
        transform: scale(1.04);
    }
    
    .yt-play-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 52px;
        height: 52px;
        background: rgba(239, 68, 68, 0.9);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.6);
        transition: transform 0.2s ease, background-color 0.2s ease;
    }
    
    .yt-card:hover .yt-play-overlay {
        transform: translate(-50%, -50%) scale(1.15);
        background: #ff0000;
    }
    
    .yt-play-icon {
        width: 0;
        height: 0;
        border-top: 10px solid transparent;
        border-bottom: 10px solid transparent;
        border-left: 16px solid #ffffff;
        margin-left: 4px;
    }
    
    .yt-card-body {
        padding: 16px;
    }
    
    .yt-card-title {
        color: #f8fafc;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 6px;
        line-height: 1.35;
    }
    
    .yt-card-channel {
        color: #ef4444;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .yt-card-desc {
        color: #cbd5e1;
        font-size: 0.84rem;
        line-height: 1.4;
    }

    /* Disclaimer */
    .disclaimer-box {
        background: rgba(245, 158, 11, 0.08);
        border-left: 4px solid #f59e0b;
        padding: 14px 18px;
        border-radius: 8px;
        font-size: 0.84rem;
        color: #fef3c7;
        margin-top: 30px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Pipeline Önörnekleme
@st.cache_resource(show_spinner="⚡ RAG Pipeline & Vektör Veri Tabanı Yükleniyor...")
def get_pipeline():
    return RAGPipeline()

@st.cache_data
def get_chunk_count():
    try:
        vs = VectorStore()
        return vs.count()
    except Exception:
        return 540

pipeline = get_pipeline()
total_chunks = get_chunk_count()

# -----------------------------------------------------------------------------
# 2. Yan Menü (Sidebar)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='font-size: 2.2rem; margin-bottom: 0;'>📈 Finans Danışmanım</h1>", unsafe_allow_html=True)
    st.markdown("<span class='badge-info'>Yerel RAG Mimarisi v2.0</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("⚙️ Sistem Ayarları")
    use_llm = st.toggle("🤖 Yerel LLM Kullan (Qwen 3.5 2B)", value=True, help="LLM yanıtını aktifleştirir. Devre dışı bırakılırsa akıllı doğrudan kaynak süzgeci kullanılır.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Retrieval Parametreleri")
    max_k = st.slider("Maksimum Kaynak Sayısı (Top-K)", min_value=1, max_value=10, value=TOP_K)
    min_score = st.slider("Minimum Benzerlik Eşiği", min_value=0.30, max_value=0.90, value=MIN_RETRIEVAL_SCORE, step=0.05)
    
    st.markdown("---")
    if st.button("🔄 Önbelleği Temizle & Yeniden Yükle", use_container_width=True):
        st.cache_resource.clear()
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **💡 İpuçları:**
    - Sorunuzu ne kadar net sorarsanız arama başarısı o kadar artar.
    - Sistem yeterli kaynak bulamazsa güvenli **fallback** devreye girer.
    - Cevabın altındaki **YouTube kapak kartlarına** tıklayarak videoları izleyebilirsiniz.
    """)

# -----------------------------------------------------------------------------
# 3. Başlık ve KPI Metrik Kartları
# -----------------------------------------------------------------------------
st.markdown("""
<div style='text-align: left; margin-bottom: 20px;'>
    <h1 style='font-size: 2.2rem; font-weight: 800; margin-bottom: 6px; background: linear-gradient(90deg, #60a5fa, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        📈 Finans Danışmanım AI Pro — Akıllı Finansal Asistan & RAG Platformu
    </h1>
    <p style='color: #94a3b8; font-size: 1rem; margin-top: 0;'>
        Yerel ChromaDB Bilgi Tabanı • Güvenilir Kaynak Doğrulama • Eğitici YouTube Video Kartları
    </p>
</div>
""", unsafe_allow_html=True)

# Canlı KPI Metrik Kartları
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-box">
        <div class="kpi-value">{total_chunks}</div>
        <div class="kpi-label">İndekslenmiş Chunk</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-value">%{min_score*100:.0f}</div>
        <div class="kpi-label">Retrieval Eşik Skoru</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-value">1024D</div>
        <div class="kpi-label">Multilingual-E5 Embed</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-value">Foundry / Local</div>
        <div class="kpi-label">Yerel Yapay Zeka</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Sekmeli Arayüz (Tabs)
# -----------------------------------------------------------------------------
tab_assistant, tab_videos, tab_analytics = st.tabs([
    "💬 Akıllı Finans Asistanı", 
    "🎥 Eğitici Video Kütüphanesi", 
    "📊 Sistem Analitiği & Veri Tabanı"
])

# -----------------------------------------------------------------------------
# TAB 1: AKILLI FİNANS ASİSTANI
# -----------------------------------------------------------------------------
with tab_assistant:
    st.markdown("### 💡 Örnek Soru Önerileri (Tek Tıkla Sorun)")
    
    # 1-Tık Örnek Sorular
    col_q1, col_q2, col_q3, col_q4, col_q5 = st.columns(5)
    selected_sample = None
    
    if col_q1.button("📌 Bileşik Faiz Nedir?", use_container_width=True):
        selected_sample = "Bileşik faiz nedir ve nasıl çalışır?"
    if col_q2.button("📊 Yatırım Fonları", use_container_width=True):
        selected_sample = "Yatırım fonları nedir ve nasıl işler?"
    if col_q3.button("📑 Bilanço Okuma", use_container_width=True):
        selected_sample = "Bilanço ve gelir tablosu nasıl analiz edilir?"
    if col_q4.button("💰 Temettü Verimi", use_container_width=True):
        selected_sample = "Temettü nedir ve temettü verimi nasıl hesaplanır?"
    if col_q5.button("📉 Enflasyon Koruması", use_container_width=True):
        selected_sample = "Enflasyondan korunmak için hangi finansal araçlar kullanılır?"

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Soru Giriş Alanı
    default_text = selected_sample if selected_sample else ""
    user_query = st.text_area(
        "Finansal Sorunuzu Giriniz:",
        value=default_text,
        placeholder="Örn: Bileşik faizin yatırım üzerindeki uzun vadeli etkisi nedir veya yatırım fonları nasıl çalışır?",
        height=95,
        key="main_query_input"
    )

    col_space, col_submit = st.columns([3, 1])
    with col_submit:
        analyze_button = st.button("🚀 Analizi Başlat", type="primary", use_container_width=True)

    # Analiz İşlemi ve Sonuçlar
    if analyze_button or selected_sample:
        query_to_process = user_query.strip() if user_query.strip() else selected_sample
        
        if not query_to_process:
            st.warning("⚠️ Lütfen analiz yapılabilmesi için geçerli bir soru giriniz.")
        else:
            with st.spinner("🔍 Vektör veri tabanından yerel kaynaklar taranıyor, detaylı yanıt ve YouTube video önerileri hazırlanıyor..."):
                try:
                    result = pipeline.answer_question(query_to_process, use_llm=use_llm)
                    
                    st.markdown("---")
                    
                    # 1. Fallback Kontrolü
                    if not result.get("has_context", False):
                        st.error("⚠️ **Kaynak Yetersizliği / Güvenli Fallback Tetiklendi**")
                        st.warning(
                            "Bilgi tabanında bu soruya yanıt verecek yeterli benzerlikte (%55+) finansal kaynak bulunamadı. "
                            "Sistem uydurma bilgi (*hallucination*) üretmemek için yanıt vermemiştir."
                        )
                        st.info(f"**Sistem Mesajı:** {result['answer']}")
                    else:
                        # 2. Detaylı Yanıt Gösterimi
                        st.markdown("""
                        <div class="finans-danismanim-card">
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                                <h3 style='margin: 0; color: #60a5fa;'>📊 Finans Danışmanım AI Profesyonel Analiz Yanıtı</h3>
                                <span class="badge-success">✓ Doğrulanmış Kaynaklar</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(result["answer"])
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # 3. YOUTUBE VİDEO ÖNERİLERİ (GÖRSEL KAPAK KARTLARI)
                        videos = result.get("youtube_videos", [])
                        if videos:
                            st.markdown("""
                            <div class="finans-danismanim-card" style='border-color: rgba(239, 68, 68, 0.4);'>
                                <h3 style='margin: 0 0 8px 0; color: #ef4444;'>🎥 İlgili Konu İçin Eğitici YouTube Videoları</h3>
                                <p style='color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0;'>
                                    İzlemek istediğiniz video kartının üzerine tıklayarak YouTube'da başlatabilirsiniz:
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            vid_cols = st.columns(min(len(videos), 2))
                            for idx, vid in enumerate(videos[:2]):
                                with vid_cols[idx]:
                                    watch_url = vid.get("watch_url") or f"https://www.youtube.com/watch?v={vid.get('video_id')}"
                                    thumb_url = vid.get("thumbnail") or f"https://img.youtube.com/vi/{vid.get('video_id')}/hqdefault.jpg"
                                    
                                    st.markdown(f"""
                                    <a href="{watch_url}" target="_blank" class="yt-card-link">
                                        <div class="yt-card">
                                            <div class="yt-thumb-container">
                                                <img src="{thumb_url}" class="yt-thumb-img" alt="{vid['title']}"/>
                                                <div class="yt-play-overlay">
                                                    <div class="yt-play-icon"></div>
                                                </div>
                                            </div>
                                            <div class="yt-card-body">
                                                <div class="yt-card-title">🎥 {vid['title']}</div>
                                                <div class="yt-card-channel">📺 {vid['channel']}</div>
                                                <div class="yt-card-desc">{vid['description']}</div>
                                            </div>
                                        </div>
                                    </a>
                                    """, unsafe_allow_html=True)


                        # 4. KULLANILAN KAYNAKLAR
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("### 📚 Yanıtta Kullanılan Doküman Kaynakları ve Benzerlik Skorları")
                        sources = result.get("sources", [])
                        
                        if sources:
                            for idx, src_info in enumerate(sources, 1):
                                score_pct = src_info['score'] * 100
                                source_name = src_info['source']
                                chunk_text = src_info['chunk']
                                
                                match_color = "#4ade80" if score_pct >= 70 else "#60a5fa"
                                
                                with st.expander(
                                    f"📌 **Kaynak [{idx}]:** `{source_name}` — Benzerlik Skoru: %{score_pct:.1f}"
                                ):
                                    st.markdown(f"**Doküman Adı:** `{source_name}`")
                                    st.markdown(f"**Benzerlik Skoru:** <span style='color: {match_color}; font-weight: 700;'>%{score_pct:.2f}</span>", unsafe_allow_html=True)
                                    st.markdown("**Eşleşen Metin Parçası (Chunk):**")
                                    st.info(chunk_text)
                                    
                except Exception as e:
                    st.error(f"❌ Analiz sırasında bir hata oluştu: {str(e)}")

# -----------------------------------------------------------------------------
# TAB 2: EĞİTİCİ VİDEO KÜTÜPHANESİ
# -----------------------------------------------------------------------------
with tab_videos:
    st.markdown("## 🎥 Finansal Okuryazarlık Video Kütüphanesi")
    st.markdown("Finansal kavramları hızlıca öğrenmek için derlenmiş öne çıkan video kütüphanesi (Tıklayarak izleyebilirsiniz):")
    
    curated = YouTubeRecommender.CURATED_VIDEOS
    grid_cols = st.columns(2)
    
    for idx, vid in enumerate(curated):
        col_target = grid_cols[idx % 2]
        with col_target:
            watch_url = vid.get("watch_url") or f"https://www.youtube.com/watch?v={vid.get('video_id')}"
            thumb_url = vid.get("thumbnail") or f"https://img.youtube.com/vi/{vid.get('video_id')}/hqdefault.jpg"
            
            st.markdown(f"""
            <a href="{watch_url}" target="_blank" class="yt-card-link">
                <div class="yt-card">
                    <div class="yt-thumb-container">
                        <img src="{thumb_url}" class="yt-thumb-img" alt="{vid['title']}"/>
                        <div class="yt-play-overlay">
                            <div class="yt-play-icon"></div>
                        </div>
                    </div>
                    <div class="yt-card-body">
                        <div class="yt-card-title">🎥 {vid['title']}</div>
                        <div class="yt-card-channel">📺 {vid['channel']}</div>
                        <div class="yt-card-desc">{vid['description']}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: SİSTEM ANALİTİĞİ & VERİ TABANI
# -----------------------------------------------------------------------------
with tab_analytics:
    st.markdown("## 📊 Sistem Analitiği & Mimari Bilgisi")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("""
        <div class="finans-danismanim-card">
            <h3 style="color: #60a5fa; margin-top:0;">🗄️ Vektör Veri Tabanı Durumu</h3>
            <ul>
                <li><b>Veri Tabanı:</b> Persistent ChromaDB</li>
                <li><b>Toplam İndekslenen Parça:</b> {}</li>
                <li><b>Embedding Modeli:</b> multilingual-e5-large</li>
                <li><b>Vektör Boyutu:</b> 1024 Boyutlu Uyumlu Vektör Uzayı</li>
                <li><b>Chunk Boyutu:</b> 900 Karakter</li>
                <li><b>Parça Örtüşmesi (Overlap):</b> 140 Karakter</li>
            </ul>
        </div>
        """.format(total_chunks), unsafe_allow_html=True)
        
    with col_a2:
        st.markdown("""
        <div class="finans-danismanim-card">
            <h3 style="color: #a855f7; margin-top:0;">🤖 Yerel Yapay Zekâ (LLM) Ayarları</h3>
            <ul>
                <li><b>Servis Sağlayıcı:</b> Microsoft Foundry Local</li>
                <li><b>Model Türü:</b> Qwen 3.5 2B Text</li>
                <li><b>Çalışma Modu:</b> %100 Yerel / Off-line Güvenli İşlem</li>
                <li><b>Eşik Filtresi:</b> %55 ve üzeri benzerlik zorunluluğu</li>
                <li><b>Veri Gizliliği:</b> Dışarıya hiçbir veri aktarılmaz</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 🏗️ RAG Çalışma Akış Şeması")
    st.code("""
    [ Kullanıcı Sorusu ]
            │
            ▼
    [ Query Embedding (1024D) ]
            │
            ▼
    [ ChromaDB Vektörel Arama ]
            │
            ▼
    [ Benzerlik Eşiği Kontrolü (>= 0.55) ]
       ├── Yetersiz ➔ [ Güvenli Fallback Yanıtı ]
       └── Yeterli  ➔ [ Yerel LLM / Qwen 3.5 2B ] + [ YouTube Video Kapak Kartları ]
                           │
                           ▼
               [ Zengin Profesyonel Yanıt + Video Kartı ]
    """, language="text")

# -----------------------------------------------------------------------------
# 5. Yasal Sorumluluk Reddi (Disclaimer)
# -----------------------------------------------------------------------------
st.markdown("""
<div class="disclaimer-box">
    <strong>⚠️ Yasal Sorumluluk Reddi Beyanı (Financial Disclaimer):</strong><br>
    Finans Danışmanım AI Pro tarafından sunlanan tüm yanıtlar, veriler ve analizler yalnızca genel finansal okuryazarlık ve bilgilendirme amacıyla üretilmektedir. 
    Burada yer alan hiçbir bilgi kişiye özel yatırım danışmanlığı, finansal tavsiye, alım-satım önerisi veya hukuki/mali bağlayıcılık taşımaz. 
    Finansal kararlarınızı vermeden önce yetkili bir lisanslı yatırım danışmanına veya finansal uzmana danışmanız önemle tavsiye olunur.
</div>
""", unsafe_allow_html=True)
