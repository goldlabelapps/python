"""Unit and integration tests for NX AI routes."""

from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.routes import get_db_connection
from app.main import app

client = TestClient(app)


def _mock_db_dependency(rows=None):
    """Return a FastAPI dependency override that yields a mock DB connection."""
    if rows is None:
        rows = []

    def override():
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = rows
        yield mock_conn

    return override


def test_root_returns_product_data() -> None:
    """GET / should return meta and data with product list."""
    app.dependency_overrides[get_db_connection] = _mock_db_dependency(rows=[])
    try:
        response = client.get("/")
        assert response.status_code == 200
        body = response.json()
        assert "meta" in body
        assert "data" in body
        assert body["meta"]["severity"] == "success"
        assert isinstance(body["data"], list)
    finally:
        app.dependency_overrides.clear()


def test_root_returns_products_from_db() -> None:
    """GET / should include product rows returned by the database."""
    from datetime import datetime
    from decimal import Decimal
    mock_row = (1, "Widget", "A useful widget", Decimal("19.99"), True, datetime(2024, 1, 1, 0, 0, 0))
    app.dependency_overrides[get_db_connection] = _mock_db_dependency(rows=[mock_row])
    try:
        response = client.get("/")
        assert response.status_code == 200
        body = response.json()
        assert len(body["data"]) == 1
        assert body["data"][0]["name"] == "Widget"
        assert body["data"][0]["price"] == "19.99"
        assert "Returned 1 products" in body["meta"]["message"]
    finally:
        app.dependency_overrides.clear()


def test_health_returns_ok() -> None:
    """GET /health should return status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_echo_returns_message() -> None:
    """POST /echo should return the provided message."""
    response = client.post("/echo", json={"message": "hello"})
    assert response.status_code == 200
    assert response.json() == {"echo": "hello"}


def test_echo_empty_string() -> None:
    """POST /echo with an empty string should echo back an empty string."""
    response = client.post("/echo", json={"message": ""})
    assert response.status_code == 200
    assert response.json() == {"echo": ""}


def test_echo_missing_body_returns_422() -> None:
    """POST /echo without a body should return 422 Unprocessable Entity."""
    response = client.post("/echo", json={})
    assert response.status_code == 422
