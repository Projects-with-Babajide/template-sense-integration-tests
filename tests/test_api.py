"""API endpoint tests for FastAPI application."""

from __future__ import annotations

import io
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app, analyzer_service

client = TestClient(app)


@pytest.fixture
def sample_file_path() -> Path:
    return Path(__file__).parent / "fixtures" / "sample_template.xlsx"


@pytest.fixture
def mock_analyzer(monkeypatch):
    """Mock the analyzer service for success case testing."""

    def _mock_analyze(file_path: str):
        return {
            "status": "ok",
            "file": str(file_path),
            "metadata": {"header_fields": ["invoice_number", "invoice_date"]},
        }

    monkeypatch.setattr(analyzer_service, "analyze", _mock_analyze)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_root_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_analyze_success(sample_file_path, mock_analyzer):
    """Test successful file analysis with mocked analyzer."""
    with sample_file_path.open("rb") as file_handle:
        response = client.post(
            "/analyze", files={"file": (sample_file_path.name, file_handle)}
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["metadata"]["header_fields"] == [
        "invoice_number",
        "invoice_date",
    ]


def test_analyze_invalid_extension():
    fake_file = io.BytesIO(b"content")
    response = client.post(
        "/analyze", files={"file": ("invalid.txt", fake_file, "text/plain")}
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert "Invalid file type" in payload["error"]


def test_analyze_missing_file():
    response = client.post("/analyze", files={})

    assert response.status_code == 422


def test_analyze_oversize_file():
    big_content = b"0" * (11 * 1024 * 1024)
    response = client.post(
        "/analyze",
        files={"file": ("big.xlsx", big_content, "application/vnd.ms-excel")},
    )

    assert response.status_code == 400
    payload = response.json()
    assert "too large" in payload["error"].lower()
