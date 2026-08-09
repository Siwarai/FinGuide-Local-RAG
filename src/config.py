# src/config.py

# LLM Ayarları
LLM_MODEL = "qwen3.5-2b-text"

# Embedding Ayarları
EMBEDDING_MODEL = "intfloat/multilingual-e5-large"
EMBEDDING_DIM = 1024

# Chunking (Metin Parçalama) Ayarları
CHUNK_SIZE = 900
CHUNK_OVERLAP = 140

# Retrieval (Geri Getirme) Ayarları
TOP_K = 4
MIN_RETRIEVAL_SCORE = 0.55
