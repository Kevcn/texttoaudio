from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "message": "Text to Audio API is running"
    }

def test_get_languages():
    """Test the languages endpoint"""
    response = client.get("/api/v1/tts/languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert isinstance(data["languages"], list)
    # Check if English is in the languages list
    assert any(lang["code"] == "en" for lang in data["languages"]) 