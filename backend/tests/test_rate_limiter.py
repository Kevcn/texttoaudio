import pytest
from fastapi.testclient import TestClient
from app.main import app
import asyncio
import time

client = TestClient(app)

def test_rate_limiter_normal_usage():
    """Test that normal usage within rate limits works"""
    # Make several requests within the limit
    for _ in range(10):
        response = client.get("/")
        assert response.status_code == 200

def test_rate_limiter_exceeds_limit():
    """Test that exceeding rate limits returns 429 status"""
    # Make many requests quickly to exceed the rate limit
    responses = []
    for _ in range(150):  # Exceeds both the per-minute and burst limit
        responses.append(client.get("/"))
    
    # Verify that some requests were rate limited
    assert any(r.status_code == 429 for r in responses)
    assert any("Too many requests" in r.json()["detail"] for r in responses if r.status_code == 429)

def test_rate_limiter_recovery():
    """Test that rate limits reset after waiting"""
    # First, hit the rate limit
    for _ in range(100):
        client.get("/")
    
    # Wait for a bit to allow the rate limit to reset
    time.sleep(2)
    
    # Try another request, should succeed
    response = client.get("/")
    assert response.status_code == 200

def test_different_ips_separate_limits():
    """Test that different IPs have separate rate limits"""
    # Make requests from two different IPs
    headers1 = {"X-Forwarded-For": "1.1.1.1"}
    headers2 = {"X-Forwarded-For": "2.2.2.2"}
    
    # Make requests from first IP
    for _ in range(50):
        response = client.get("/", headers=headers1)
        assert response.status_code == 200
    
    # Make requests from second IP
    for _ in range(50):
        response = client.get("/", headers=headers2)
        assert response.status_code == 200 