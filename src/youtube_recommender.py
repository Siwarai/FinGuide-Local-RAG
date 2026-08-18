"""
Finans Danışmanım AI - YouTube Eğitici Video Öneri Modülü
Kullanıcı sorularından finansal anahtar kelimeleri tespit eder ve YouTube üzerinden
canlı arama gerçekleştirerek konuya en özel eğitici videoları getirir.
Spesifik video bulunamadığında veya ağ hatalarında en yakın konsept videolarına yönlendirir.
"""

import json
import re
import urllib.parse
import urllib.request
import random
from typing import List, Dict, Any, Optional


class YouTubeRecommender:
    """
    Finansal okuryazarlık konuları için Canlı YouTube Arama Motoru
    ve akıllı yedekleme (fallback) sistemi.
    """
    
    _CACHE: Dict[str, List[Dict[str, Any]]] = {}

    # %100 Canlı, resmi Türkçe finans ve yatırım eğitimi videoları (Yedek kütüphane)
    CURATED_VIDEOS: List[Dict[str, Any]] = [
        {
            "keywords": ["tkm", "tefas", "befas", "yatırım fonu", "yatırım fonları", "fon", "portföy", "teb", "banka fonu", "para piyasası"],
            "title": "TEFAS Nedir ve Nasıl Kullanılır? Yatırım Fonları Eğitimi #9",
            "channel": "Finans ve Borsa",
            "video_id": "MA6Je2zubYM",
            "watch_url": "https://www.youtube.com/watch?v=MA6Je2zubYM",
            "thumbnail": "https://img.youtube.com/vi/MA6Je2zubYM/hqdefault.jpg",
            "description": "Yatırım fonları, TEFAS ve BEFAS sisteminin çalışma prensipleri ve fon seçimi rehberi."
        },
        {
            "keywords": ["bileşik faiz", "bilesik faiz", "paranın zaman değeri", "faiz getirisi", "anapara", "faiz"],
            "title": "Bileşik Faiz ile Zengin Olmak: 5 Yıllık Strateji",
            "channel": "Akıllı Yatırımcı",
            "video_id": "D_08X6E3bok",
            "watch_url": "https://www.youtube.com/watch?v=D_08X6E3bok",
            "thumbnail": "https://img.youtube.com/vi/D_08X6E3bok/hqdefault.jpg",
            "description": "Bileşik faizin üstel büyüme gücünü ve uzun vadeli birikimlerdeki etkisini anlatan anlaşılır rehber."
        },
        {
            "keywords": ["enflasyon", "tüfe", "üfe", "satın alma gücü", "fiyat artışı", "değer kaybı"],
            "title": "Enflasyon Nedir? Mahfi Eğilmez ile Ekonomi 101",
            "channel": "Mahfi Eğilmez • Ekonomi Dersleri",
            "video_id": "DFJjzAyIEGk",
            "watch_url": "https://www.youtube.com/watch?v=DFJjzAyIEGk",
            "thumbnail": "https://img.youtube.com/vi/DFJjzAyIEGk/hqdefault.jpg",
            "description": "Enflasyonun nedenleri, tüketici fiyat endeksi (TÜFE) ve birikimleri enflasyondan koruma yöntemleri."
        },
        {
            "keywords": ["bilanço", "bilanco", "gelir tablosu", "finansal tablo", "faök", "ebitda", "net kar", "özkaynak", "varlıklar"],
            "title": "Bilanço Analizi Yapılırken Dikkat Edilmesi Gerekenler",
            "channel": "Borsa ve Bilanço Okuma",
            "video_id": "NBlYpnaFgwg",
            "watch_url": "https://www.youtube.com/watch?v=NBlYpnaFgwg",
            "thumbnail": "https://img.youtube.com/vi/NBlYpnaFgwg/hqdefault.jpg",
            "description": "Varlıklar, yükümlülükler, özkaynaklar ve gelir tablosundaki kritik kalemlerin detaylı incelemesi."
        },
        {
            "keywords": ["temettü", "temettu", "kar payı", "temettü verimi", "temettü emekliliği"],
            "title": "Temettü Nedir? Temettü Yatırımı Nasıl Yapılır?",
            "channel": "Temettü Yatırımcısı",
            "video_id": "MG-cwxwWpXc",
            "watch_url": "https://www.youtube.com/watch?v=MG-cwxwWpXc",
            "thumbnail": "https://img.youtube.com/vi/MG-cwxwWpXc/hqdefault.jpg",
            "description": "Şirketlerin kâr payı dağıtımı, temettü verimi hesaplama ve sürdürülebilir temettü şirketleri."
        },
        {
            "keywords": ["borsa", "hisse senedi", "hisse", "bist", "bist100", "alım satım", "yatırım"],
            "title": "Borsa Yatırımı Nasıl Yapılır? | Prof. Dr. Emre Alkin",
            "channel": "Borsa Okulu",
            "video_id": "7_zed4XMLAE",
            "watch_url": "https://www.youtube.com/watch?v=7_zed4XMLAE",
            "thumbnail": "https://img.youtube.com/vi/7_zed4XMLAE/hqdefault.jpg",
            "description": "Hisse senedi nedir, borsa nasıl çalışır ve ilk hisse alımında dikkat edilmesi gereken noktalar."
        },
        {
            "keywords": ["befas", "fon alım", "banka fonu", "para piyasası fonu", "borçlanma araçları"],
            "title": "TEFAS ve BEFAS Bilmeden Yatırım Yapmayın!",
            "channel": "Yatırım Akademisi",
            "video_id": "33b-YzQjeow",
            "watch_url": "https://www.youtube.com/watch?v=33b-YzQjeow",
            "thumbnail": "https://img.youtube.com/vi/33b-YzQjeow/hqdefault.jpg",
            "description": "Banka yatırım fonları ve fon alım satımında dikkat edilmesi gereken noktalar."
        }
    ]

    @classmethod
    def search_youtube_live(cls, search_term: str, limit: int = 2) -> List[Dict[str, Any]]:
        """
        YouTube üzerinden arama terimiyle canlı video araması yapar.
        """
        try:
            q = urllib.parse.quote(search_term)
            url = f"https://www.youtube.com/results?search_query={q}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                html = resp.read().decode("utf-8")
                
            m = re.search(r'ytInitialData\s*=\s*({.*?});(?:</script>|var )', html)
            if not m:
                return []
                
            data = json.loads(m.group(1))
            sections = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
            
            results = []
            seen_ids = set()
            
            for sec in sections:
                item_sec = sec.get("itemSectionRenderer", {}).get("contents", [])
                for item in item_sec:
                    if "videoRenderer" in item:
                        vr = item["videoRenderer"]
                        v_id = vr.get("videoId")
                        if not v_id or v_id in seen_ids:
                            continue
                            
                        title_runs = vr.get("title", {}).get("runs", [])
                        title = title_runs[0].get("text", "") if title_runs else ""
                        
                        owner_runs = vr.get("ownerText", {}).get("runs", [])
                        channel = owner_runs[0].get("text", "YouTube Finans") if owner_runs else "YouTube Finans"
                        
                        desc = ""
                        if "detailedMetadataSnippets" in vr and vr["detailedMetadataSnippets"]:
                            d_runs = vr["detailedMetadataSnippets"][0].get("snippetText", {}).get("runs", [])
                            desc = "".join([r.get("text", "") for r in d_runs])
                        elif "descriptionSnippet" in vr:
                            d_runs = vr["descriptionSnippet"].get("runs", [])
                            desc = "".join([r.get("text", "") for r in d_runs])
                            
                        if not desc:
                            desc = f"{search_term} hakkında eğitici video içeriği."
                            
                        if len(desc) > 130:
                            desc = desc[:127] + "..."
                            
                        results.append({
                            "video_id": v_id,
                            "title": title,
                            "channel": channel,
                            "watch_url": f"https://www.youtube.com/watch?v={v_id}",
                            "thumbnail": f"https://img.youtube.com/vi/{v_id}/hqdefault.jpg",
                            "description": desc
                        })
                        seen_ids.add(v_id)
                        
                        if len(results) >= limit:
                            break
                if len(results) >= limit:
                    break
                    
            return results
        except Exception:
            return []

    @classmethod
    def get_recommendations(cls, query: str, limit: int = 2) -> List[Dict[str, Any]]:
        """
        Kullanıcı sorusuna en uygun YouTube videolarını getirir:
        1. Önce doğrudan kullanıcının sorgusu ile canlı YouTube araması yapar.
        2. Sonuç yetersizse daha genel/yakın bir finansal kavram araması (örn: "yatırım fonları nedir") dener.
        3. Ağ hatası veya erişim engeli durumunda static kütüphaneden akıllı seçim yapar.
        """
        if not query:
            return cls._get_curated_fallback(query, limit)

        clean_query = query.strip()
        cache_key = f"{clean_query.lower()}_{limit}"
        if cache_key in cls._CACHE:
            return cls._CACHE[cache_key]

        # 1. Aşama: Doğrudan Sorgu ile Canlı YouTube Araması
        live_results = cls.search_youtube_live(clean_query, limit=limit)
        
        # Eğer yeterli video bulunduysa döndür
        if len(live_results) >= limit:
            cls._CACHE[cache_key] = live_results
            return live_results

        # 2. Aşama: Konu Türetme / Yakın Kavram Arama Fallback'i
        broader_query = cls._extract_broader_query(clean_query)
        if broader_query and broader_query.lower() != clean_query.lower():
            broader_results = cls.search_youtube_live(broader_query, limit=limit)
            combined = live_results + [v for v in broader_results if v["video_id"] not in {x["video_id"] for x in live_results}]
            if len(combined) >= limit:
                cls._CACHE[cache_key] = combined[:limit]
                return combined[:limit]
            live_results = combined

        # 3. Aşama: Curated List / Offline Fallback
        curated_fallbacks = cls._get_curated_fallback(clean_query, limit=limit)
        combined_final = live_results + [v for v in curated_fallbacks if v.get("video_id") not in {x.get("video_id") for x in live_results}]
        final_result = combined_final[:limit]
        
        cls._CACHE[cache_key] = final_result
        return final_result

    @classmethod
    def _extract_broader_query(cls, query: str) -> Optional[str]:
        """Sorgudaki anahtar kelimelere bakarak daha geniş bir arama terimi türetir."""
        q_lower = query.lower()
        if any(kw in q_lower for kw in ["fon", "tkm", "tefas", "befas", "portföy"]):
            return "yatırım fonları nedir eğitimi"
        if any(kw in q_lower for kw in ["faiz", "bileşik", "mevduat"]):
            return "bileşik faiz ve birikim rehberi"
        if any(kw in q_lower for kw in ["borsa", "hisse", "bist"]):
            return "borsa ve hisse senedi yatırımı nasıl yapılır"
        if any(kw in q_lower for kw in ["enflasyon", "tüfe", "paranın değeri"]):
            return "enflasyon nedir birikimleri koruma"
        if any(kw in q_lower for kw in ["bilanço", "gelir tablosu", "ebitda"]):
            return "bilanço okuma ve şirket analizi"
        if any(kw in q_lower for kw in ["temettü", "kâr payı"]):
            return "temettü yatırımı nedir"
        return "finansal okuryazarlık temel eğitimi"

    @classmethod
    def _get_curated_fallback(cls, query: str, limit: int = 2) -> List[Dict[str, Any]]:
        """Static curated listeden sorguya en uygun ve çeşitlendirilmiş videoları seçer."""
        clean_query = query.lower() if query else ""
        matched = []
        
        for item in cls.CURATED_VIDEOS:
            for kw in item.get("keywords", []):
                if kw in clean_query:
                    if item not in matched:
                        matched.append(item)
                    break
                    
        unmatched = [v for v in cls.CURATED_VIDEOS if v not in matched]
        
        seed = sum(ord(c) for c in clean_query) if clean_query else 42
        rng = random.Random(seed)
        rng.shuffle(unmatched)
        
        result = matched + unmatched
        return result[:limit]

