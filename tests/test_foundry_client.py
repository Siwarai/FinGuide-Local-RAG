import pytest
from unittest.mock import patch, MagicMock
from src.foundry_client import FoundryClient  # pyrefly: ignore [missing-import]

def test_foundry_client_initialization():
    client = FoundryClient()
    assert client.base_url is not None
    assert client.model is not None

def test_foundry_client_connection_error_fallback():
    client = FoundryClient(base_url="http://invalid-localhost-port-99999/v1")
    answer = client.generate_answer("System prompt", "Context", "Query")
    assert answer is None


def test_foundry_client_successful_response():
    client = FoundryClient()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {"message": {"content": "Bu bir test yanıtıdır."}}
        ]
    }
    
    with patch("requests.post", return_value=mock_response):
        answer = client.generate_answer("System prompt", "Context", "Query")
        assert answer == "Bu bir test yanıtıdır."
