import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_prospects_init_returns_placeholder():
    response = client.get("/prospects/init")
    assert response.status_code == 200
    data = response.json()
    assert "meta" in data
    assert "data" in data
    assert data["data"]["message"] == "This is a placeholder for prospects/init."

def test_prospects_returns_list():
    response = client.get("/prospects")
    assert response.status_code == 200
    data = response.json()
    assert "meta" in data
    assert "data" in data
    assert isinstance(data["data"], list) or isinstance(data["data"], dict)

def test_prospects_unique_valid_fields():
    # This test assumes at least one valid field exists in the prospects table, e.g., 'id'.
    response = client.get("/prospects/unique?fields=id")
    assert response.status_code == 200
    data = response.json()
    assert "meta" in data
    assert "data" in data
    assert isinstance(data["data"], dict)

def test_prospects_unique_invalid_field():
    response = client.get("/prospects/unique?fields=notafield")
    assert response.status_code == 200
    data = response.json()
    assert "meta" in data
    assert "errors" in data
    assert "notafield" in data["errors"]

def test_prospects_init_meta_keys():
    response = client.get("/prospects/init")
    meta = response.json()["meta"]
    for key in ["severity", "title", "version", "base_url", "time"]:
        assert key in meta
