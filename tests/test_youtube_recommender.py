import os
import sys

# Kök dizini sys.path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.youtube_recommender import YouTubeRecommender  # pyrefly: ignore [missing-import]



def test_youtube_recommender_bilesik_faiz():
    videos = YouTubeRecommender.get_recommendations("Bileşik faiz hesaplama yöntemi nedir?")
    assert isinstance(videos, list)
    assert len(videos) > 0
    title_lower = videos[0]["title"].lower()
    assert "bileşik" in title_lower or "faiz" in title_lower or "bilesik" in title_lower
    assert "watch_url" in videos[0] or "thumbnail" in videos[0]


def test_youtube_recommender_tkm_fonu():
    videos = YouTubeRecommender.get_recommendations("tkm fonu nedir")
    assert isinstance(videos, list)
    assert len(videos) > 0
    assert "watch_url" in videos[0]
    assert "thumbnail" in videos[0]


def test_youtube_recommender_fallback():
    videos = YouTubeRecommender.get_recommendations("Bilinmeyen garip bir finans konusu 9999")
    assert isinstance(videos, list)
    assert len(videos) > 0
    assert "watch_url" in videos[0] or "thumbnail" in videos[0]


