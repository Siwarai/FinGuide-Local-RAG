import pytest
import os
import tempfile
from src.ingest import chunk_text, read_txt  # pyrefly: ignore [missing-import]

def test_chunk_text():
    text = "A" * 1000
    chunks = chunk_text(text, chunk_size=300, chunk_overlap=50)
    assert len(chunks) > 1
    assert len(chunks[0]) == 300

def test_read_txt():
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
        tmp.write("Test metni içeriği")
        tmp_path = tmp.name

    try:
        content = read_txt(tmp_path)
        assert content == "Test metni içeriği"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
