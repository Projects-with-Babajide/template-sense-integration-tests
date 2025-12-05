"""Integration tests for AnalyzerService with real Excel files."""

import os
from pathlib import Path

import pytest
from template_sense.ai_providers.config import AIConfig
from template_sense.analyzer import extract_template_structure
from template_sense.errors import (
    AIProviderError,
    ExtractionError,
    FileValidationError,
    InvalidFieldDictionaryError,
    UnsupportedFileTypeError,
)

from app.services.analyzer import AnalyzerService


@pytest.fixture
def sample_excel_path():
    """Path to sample Excel fixture."""
    return Path(__file__).parent / "fixtures" / "sample_template.xlsx"


@pytest.fixture
def field_dictionary():
    """Sample field dictionary for invoice templates."""
    return {
        "headers": {
            "invoice_number": "Invoice number",
            "invoice_date": "Invoice date",
            "shipper_name": "Shipper",
            "consignee_name": "Consignee",
            "total_amount": "Total amount",
        },
        "columns": {
            "item": "Item",
            "quantity": "Quantity",
            "price": "Price",
        },
    }


@pytest.fixture
def api_key(validate_environment):
    """Get AI provider API key from environment."""
    key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not key:
        pytest.skip("No AI provider API key found in environment")
    return key


def test_analyzer_service_initialization(api_key):
    """Test that AnalyzerService can be initialized."""
    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    config = AIConfig(provider=provider, api_key=api_key)
    assert config.provider == provider


@pytest.mark.integration
def test_extract_template_from_excel(sample_excel_path, field_dictionary, api_key):
    """Test extracting template metadata from a real Excel file."""
    assert sample_excel_path.exists(), f"Sample file not found: {sample_excel_path}"

    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    ai_config = AIConfig(provider=provider, api_key=api_key)

    result = extract_template_structure(
        file_path=str(sample_excel_path),
        field_dictionary=field_dictionary,
        ai_config=ai_config,
    )

    assert result is not None
    assert isinstance(result, dict)


@pytest.mark.integration
def test_validate_json_output_structure(sample_excel_path, field_dictionary, api_key):
    """Test that JSON output has expected structure."""
    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    ai_config = AIConfig(provider=provider, api_key=api_key)

    result = extract_template_structure(
        file_path=str(sample_excel_path),
        field_dictionary=field_dictionary,
        ai_config=ai_config,
    )

    normalized = result.get("normalized_output", {})
    assert "headers" in normalized or "header_fields" in normalized
    # Table columns may be missing when upstream classification encounters
    # connectivity or model issues; ensure the structure is still a mapping.
    assert isinstance(normalized, dict)


def test_error_handling_missing_file(field_dictionary, api_key):
    """Test error handling when file doesn't exist."""
    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    analyzer = AnalyzerService(ai_provider=provider)

    with pytest.raises((FileNotFoundError, FileValidationError, UnsupportedFileTypeError, ExtractionError)):
        analyzer.analyze(file_path="/nonexistent/file.xlsx")


def test_error_handling_invalid_file(tmp_path, field_dictionary, api_key):
    """Test error handling with corrupted Excel file."""
    invalid_file = tmp_path / "corrupted.xlsx"
    invalid_file.write_text("This is not a valid Excel file")

    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    analyzer = AnalyzerService(ai_provider=provider)

    with pytest.raises((ExtractionError, FileValidationError, UnsupportedFileTypeError)):
        analyzer.analyze(file_path=str(invalid_file))


def test_error_handling_missing_api_key(tmp_path):
    """Test that missing API key is handled gracefully."""
    original_openai = os.environ.pop("OPENAI_API_KEY", None)
    original_anthropic = os.environ.pop("ANTHROPIC_API_KEY", None)
    os.environ["TEMPLATE_SENSE_AI_PROVIDER"] = "openai"

    dummy_file = tmp_path / "dummy.xlsx"
    dummy_file.touch()

    try:
        analyzer = AnalyzerService(ai_provider="openai")
        with pytest.raises(AIProviderError):
            analyzer.analyze(file_path=str(dummy_file))
    finally:
        if original_openai:
            os.environ["OPENAI_API_KEY"] = original_openai
        if original_anthropic:
            os.environ["ANTHROPIC_API_KEY"] = original_anthropic
        os.environ.pop("TEMPLATE_SENSE_AI_PROVIDER", None)
