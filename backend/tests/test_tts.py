import pytest
from fastapi.testclient import TestClient
from app.main import app
import time
from pathlib import Path
from datetime import datetime, timedelta
import os

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "message": "Text to Audio API is running"
    }

def test_get_languages():
    """Test getting available languages"""
    response = client.get("/api/v1/tts/languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert isinstance(data["languages"], list)
    assert len(data["languages"]) > 0
    
    # Verify language structure
    for lang in data["languages"]:
        assert "code" in lang
        assert "name" in lang
        assert isinstance(lang["code"], str)
        assert isinstance(lang["name"], str)

def test_convert_text_empty():
    """Test converting empty text"""
    response = client.post("/api/v1/tts/convert", json={
        "text": "",
        "language": "en"
    })
    assert response.status_code == 400
    assert "detail" in response.json()

def test_convert_text_invalid_language():
    """Test converting text with invalid language"""
    response = client.post("/api/v1/tts/convert", json={
        "text": "Hello, world!",
        "language": "invalid"
    })
    assert response.status_code == 400
    assert "detail" in response.json()

def test_convert_text_success():
    """Test successful text conversion"""
    response = client.post("/api/v1/tts/convert", json={
        "text": "Hello, world!",
        "language": "en"
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert "content-disposition" in response.headers
    assert response.headers["content-disposition"].startswith("attachment; filename=")

def test_file_cleanup():
    """Test that old files are cleaned up"""
    # Create a test file that's older than the expiry time
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    test_file = output_dir / "test_old.mp3"
    test_file.touch()

    # Set file's modification time to 25 hours ago
    old_time = time.time() - (25 * 3600)  # 25 hours in seconds
    os.utime(test_file, (old_time, old_time))

    # Trigger cleanup by making a new conversion
    response = client.post("/api/v1/tts/convert", json={
        "text": "Trigger cleanup",
        "language": "en"
    })
    assert response.status_code == 200

    # Check that the old file was removed
    assert not test_file.exists()

def test_file_cleanup_keeps_recent():
    """Test that recent files are not cleaned up"""
    # Create a test file that's newer than the expiry time
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    test_file = output_dir / "test_recent.mp3"
    test_file.touch()

    # Set file's modification time to 1 hour ago
    recent_time = time.time() - (1 * 3600)  # 1 hour in seconds
    os.utime(test_file, (recent_time, recent_time))

    # Trigger cleanup by making a new conversion
    response = client.post("/api/v1/tts/convert", json={
        "text": "Trigger cleanup",
        "language": "en"
    })
    assert response.status_code == 200

    # Check that the recent file was not removed
    assert test_file.exists()

    # Clean up test file
    test_file.unlink() 