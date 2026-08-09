import os
import sys

# Kök dizini sys.path'e ekle (IDE/Linter ve import sorunlarını önlemek için)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from src.rag import RAGPipeline  # pyrefly: ignore [missing-import]



# -----------------------------------------------------------------------------
# Sayfa Konfigürasyonu & Başlık Yapılandırması
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FinGuide AI - Akıllı Finansal Asistan",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pipeline Önörnekleme (Caching - Performans için Tek Seferlik Yükleme)
@st.cache_resource(show_spinner="RAG Pipeline Bileşenleri (Embedder, VectorStore) Yükleniyor...")
def get_pipeline():
    return RAGPipeline()

pipeline = get_pipeline()

# -----------------------------------------------------------------------------
# Yan Menü (Sidebar) - Ayarlar ve Bilgilendirme
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/financial-growth-analysis.png", width=80)
    st.title("FinGuide AI")
    st.caption("Yerel RAG Mimarisi v1.0")
    
    st.markdown("---")
    st.subheader("⚙️ Sistem Parametreleri")
    use_llm = st.toggle("Yerel LLM Kullan", value=True, help="LLM yanıtını aktifleştirir. Devre dışı bırakılırsa sadece bağlam (retrieval) getirilir.")
    if st.button("🔄 Önbelleği Temizle ve Yenile", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()

    
    st.markdown("---")
    st.markdown("""
    **💡 Kullanım İpuçları:**
    - Sorunuzu ne kadar net ve spesifik sorarsanız, retrieval o kadar doğru çalışır.
    - Şirket raporları, 10-K, 10-Q veya finansal tablolar hakkındaki soruları yöneltebilirsiniz.
    - Retrieval eşik değerinin altındaki yetersiz durumlarda sistem **güvenli fallback** mekanizmasını çalıştırır.
    """)

# -----------------------------------------------------------------------------
# 1. FinGuide AI Başlığı ve Kısa Amaç Açıklaması
# -----------------------------------------------------------------------------
st.title("📈 FinGuide AI - Finansal RAG Asistanı")
st.markdown("""
FinGuide AI, yerel veritabanınızda indekslenmiş olan finansal belgelerinizden (şirket raporları, bilançolar, analizler) 
doğrudan veri çekerek sorularınızı yanıtlayan **güvenilir ve doğrulanabilir bir RAG (Retrieval-Augmented Generation)** asistanıdır.
*Verileriniz tamamen yerelde işlenir ve dışarıya aktarılmaz.*
""")

st.markdown("---")

# -----------------------------------------------------------------------------
# 2. Finansal Soru Giriş Alanı ve Analiz Butonu
# -----------------------------------------------------------------------------
col_input, col_btn = st.columns([4, 1])

with col_input:
    user_query = st.text_area(
        "Finansal Sorunuzu Giriniz:",
        placeholder="Örn: 2023 yılı 4. çeyrek net kâr marjı ve toplam gelir tablosu detayları nedir?",
        height=100,
        key="query_input"
    )

st.markdown("<br>", unsafe_allow_html=True)
analyze_button = st.button("🚀 Analizi Başlat", type="primary", use_container_width=True)

# -----------------------------------------------------------------------------
# İşlem Mantığı ve Sonuçların Gösterimi
# -----------------------------------------------------------------------------
if analyze_button:
    if not user_query.strip():
        st.warning("⚠️ Lütfen analiz yapılabilmesi için geçerli bir soru giriniz.")
    else:
        # 3. Yükleniyor / İşlem Durumu Göstergesi
        with st.spinner("🔍 Finansal dokümanlar taranıyor, vektörel benzerlik hesaplanıyor ve yanıt üretiliyor..."):
            try:
                # 4. RAGPipeline sınıfı üzerinden yanıtın üretilmesi
                result = pipeline.answer_question(user_query, use_llm=use_llm)
                
                st.markdown("### 📊 Analiz Sonucu")
                
                # 6. Kaynak Yetersizliği / Fallback Durumu Kontrolü
                if not result.get("has_context", False):
                    st.error("⚠️ **Kaynak Yetersizliği / Fallback Durumu Tetiklendi**")
                    st.warning(
                        "Bilgi tabanında girdiğiniz soruya yanıt verecek yeterli benzerlikte finansal kaynak bulunamadı. "
                        "Sistem uydurma bilgi üretmemek adına güvenli fallback yanıtını döndürmüştür."
                    )
                    st.info(f"**Sistem Yanıtı:** {result['answer']}")
                else:
                    # 4. Üretilen Yanıtın Gösterilmesi
                    st.success("✅ **Yanıt Başarıyla Üretildi**")
                    st.markdown(f"```markdown\n{result['answer']}\n```" if not use_llm else result['answer'])
                    
                    st.markdown("---")
                    
                    # 5. Kullanılan Kaynakların Listesi ve Benzerlik Skorları
                    st.markdown("### 📚 Kullanılan Kaynaklar ve Benzerlik Skorları")
                    sources = result.get("sources", [])
                    
                    if sources:
                        for idx, src_info in enumerate(sources, 1):
                            score_pct = src_info['score'] * 100
                            source_name = src_info['source']
                            chunk_text = src_info['chunk']
                            
                            with st.expander(f"📌 **Kaynak [{idx}]:** `{source_name}` — **Benzerlik Skoru:** `%{score_pct:.2f}` ({src_info['score']:.4f})"):
                                st.markdown(f"**Doküman:** `{source_name}`")
                                st.markdown(f"**Eşleşen Metin Parçası (Chunk):**")
                                st.caption(chunk_text)
                    else:
                        st.info("Bu yanıt için spesifik kaynak parçası gösterilemiyor.")
                        
            except Exception as e:
                st.error(f"❌ Analiz sırasında bir hata oluştu: {str(e)}")

# -----------------------------------------------------------------------------
# 7. Sayfa Altı Finansal Sorumluluk Reddi Beyanı (Disclaimer)
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style='background-color: rgba(255, 193, 7, 0.1); border-left: 4px solid #ffc107; padding: 12px; border-radius: 4px; font-size: 0.85rem; color: #856404;'>
    <strong>⚠️ Yasal Sorumluluk Reddi Beyanı (Financial Disclaimer):</strong><br>
    FinGuide AI tarafından sunlanan tüm yanıtlar, veriler ve analizler yalnızca genel bilgilendirme amacıyla üretilmektedir. 
    Burada yer alan hiçbir bilgi kişiye özel yatırım danışmanlığı, finansal tavsiye, alım-satım önerisi veya hukuki/mali bağlayıcılık taşımaz. 
    Finansal kararlarınızı vermeden önce yetkili bir lisanslı yatırım danışmanına veya finansal uzmana danışmanız önemle tavsiye olunur.
</div>
""", unsafe_allow_html=True)
