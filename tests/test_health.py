import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_meta_keys():
    response = client.get("/health")
    data = response.json()
    if "meta" in data:
        meta = data["meta"]
        for key in ["severity", "title", "version", "base_url", "time"]:
            assert key in meta
    else:
        # Legacy: no meta, just status
        assert data == {"status": "ok"}
