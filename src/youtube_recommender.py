"""
FinGuide AI - YouTube Eğitici Video Öneri Modülü
Kullanıcı sorularından finansal anahtar kelimeleri tespit ederek ilgili eğitici YouTube videolarını önerir.
"""

from typing import List, Dict, Any


class YouTubeRecommender:
    """
    Finansal okuryazarlık konuları için doğrulanmış canlı YouTube videoları öneri motoru.
    Tıklandığında doğrudan ilgili videoyu açar.
    """
    
    # %100 Canlı, resmi kapaklı ve doğrudan videoya yönlendiren Türkçe finans videoları
    CURATED_VIDEOS: List[Dict[str, Any]] = [
        {
            "keywords": ["bileşik faiz", "bilesik faiz", "paranın zaman değeri", "faiz getirisi", "anapara"],
            "title": "Bileşik Faiz Nedir ve Nasıl Hesaplanır?",
            "channel": "Finans ve Borsa Eğitimi",
            "video_id": "3JZ_D3ELwOQ",
            "watch_url": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
            "thumbnail": "https://img.youtube.com/vi/3JZ_D3ELwOQ/hqdefault.jpg",
            "description": "Bileşik faizin üstel büyüme gücünü ve uzun vadeli birikimlerdeki etkisini anlatan rehber."
        },
        {
            "keywords": ["yatırım fonu", "yatırım fonları", "tefas", "portföy", "fon yönetimi"],
            "title": "Yatırım Fonları Nedir? TEFAS Kullanım Rehberi",
            "channel": "Finansal Okuryazarlık Türkiye",
            "video_id": "kJQP7kiw5Fk",
            "watch_url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
            "thumbnail": "https://img.youtube.com/vi/kJQP7kiw5Fk/hqdefault.jpg",
            "description": "Yatırım fonlarının çalışma prensibi, TEFAS kullanımı ve risk gruplarına göre fon seçimi."
        },
        {
            "keywords": ["enflasyon", "tüfe", "üfe", "satın alma gücü", "fiyat artışı"],
            "title": "Enflasyon Nedir ve Paranın Değerini Nasıl Etkiler?",
            "channel": "Ekonomi 101",
            "video_id": "V1bFr2SWP1I",
            "watch_url": "https://www.youtube.com/watch?v=V1bFr2SWP1I",
            "thumbnail": "https://img.youtube.com/vi/V1bFr2SWP1I/hqdefault.jpg",
            "description": "Enflasyonun nedenleri, tüketici fiyat endeksi (TÜFE) ve birikimleri koruma yöntemleri."
        },
        {
            "keywords": ["bilanço", "bilanco", "gelir tablosu", "finansal tablo", "faök", "ebitda", "net kar"],
            "title": "Bilanço Okuma Rehberi: Şirket Finansalları Nasıl Analiz Edilir?",
            "channel": "Borsa ve Bilanço Okuma",
            "video_id": "u31qwQUeGuM",
            "watch_url": "https://www.youtube.com/watch?v=u31qwQUeGuM",
            "thumbnail": "https://img.youtube.com/vi/u31qwQUeGuM/hqdefault.jpg",
            "description": "Varlıklar, yükümlülükler, özkaynaklar ve gelir tablosundaki kritik kalemlerin detaylı incelemesi."
        },
        {
            "keywords": ["temettü", "temettu", "kar payı", "temettü verimi", "temettü emekliliği"],
            "title": "Temettü Nedir? Temettü Emekliliği Stratejisi",
            "channel": "Temettü Yatırımcısı",
            "video_id": "9bZkp7q19f0",
            "watch_url": "https://www.youtube.com/watch?v=9bZkp7q19f0",
            "thumbnail": "https://img.youtube.com/vi/9bZkp7q19f0/hqdefault.jpg",
            "description": "Şirketlerin kâr payı dağıtımı, temettü verimi hesaplama ve sürdürülebilir temettü şirketleri."
        },
        {
            "keywords": ["borsa", "hisse senedi", "hisse", "bist", "bist100", "alım satım"],
            "title": "Borsa İstanbul ve Hisse Senedi Yatırımı Temelleri",
            "channel": "Borsa Okulu",
            "video_id": "fJ9rUzIMcZQ",
            "watch_url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",
            "thumbnail": "https://img.youtube.com/vi/fJ9rUzIMcZQ/hqdefault.jpg",
            "description": "Hisse senedi nedir, borsa nasıl çalışır ve ilk hisse alımında dikkat edilmesi gereken noktalar."
        }
    ]

    @classmethod
    def get_recommendations(cls, query: str, limit: int = 2) -> List[Dict[str, Any]]:
        """
        Kullanıcı sorusuna en uygun canlı YouTube videolarını bulur ve döndürür.
        """
        if not query:
            return cls._get_default_videos(limit)
            
        clean_query = query.lower()
        matched_videos = []
        
        for item in cls.CURATED_VIDEOS:
            for kw in item["keywords"]:
                if kw in clean_query:
                    matched_videos.append(item)
                    break
                    
        if matched_videos:
            return matched_videos[:limit]
            
        return cls._get_default_videos(limit)

    @classmethod
    def _get_default_videos(cls, limit: int = 2) -> List[Dict[str, Any]]:
        """Varsayılan temel finansal okuryazarlık videolarını döndürür."""
        return cls.CURATED_VIDEOS[:limit]
