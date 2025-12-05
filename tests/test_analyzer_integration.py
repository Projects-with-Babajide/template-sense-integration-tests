"""Integration tests for AnalyzerService with real Excel files."""

import os
import pytest
from pathlib import Path
from template_sense import AnalyzerService


@pytest.fixture
def sample_excel_path():
    """Path to sample Excel fixture."""
    return Path(__file__).parent / "fixtures" / "sample_template.xlsx"


@pytest.fixture
def field_dictionary():
    """Sample field dictionary for invoice templates."""
    return {
        "invoice_number": ["invoice no", "inv no", "invoice #"],
        "invoice_date": ["date", "invoice date"],
        "shipper_name": ["shipper", "sender", "from"],
        "consignee_name": ["consignee", "receiver", "to"],
        "total_amount": ["total", "amount", "grand total"],
    }


@pytest.fixture
def api_key():
    """Get AI provider API key from environment."""
    key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not key:
        pytest.skip("No AI provider API key found in environment")
    return key


def test_analyzer_service_initialization(api_key):
    """Test that AnalyzerService can be initialized."""
    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    analyzer = AnalyzerService(ai_provider=provider)
    assert analyzer is not None


@pytest.mark.integration
def test_extract_template_from_excel(sample_excel_path, field_dictionary, api_key):
    """Test extracting template metadata from a real Excel file."""
    assert sample_excel_path.exists(), f"Sample file not found: {sample_excel_path}"

    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    analyzer = AnalyzerService(ai_provider=provider)

    result = analyzer.extract_template(
        file_path=str(sample_excel_path), field_dict=field_dictionary
    )

    assert result is not None
    assert isinstance(result, dict)


@pytest.mark.integration
def test_validate_json_output_structure(sample_excel_path, field_dictionary, api_key):
    """Test that JSON output has expected structure."""
    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    analyzer = AnalyzerService(ai_provider=provider)

    result = analyzer.extract_template(
        file_path=str(sample_excel_path), field_dict=field_dictionary
    )

    # Validate expected keys (adjust based on actual template-sense output)
    assert "header_fields" in result or "headers" in result
    assert "table_regions" in result or "tables" in result


def test_error_handling_missing_file(field_dictionary, api_key):
    """Test error handling when file doesn't exist."""
    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    analyzer = AnalyzerService(ai_provider=provider)

    with pytest.raises((FileNotFoundError, ValueError, Exception)):
        analyzer.extract_template(
            file_path="/nonexistent/file.xlsx", field_dict=field_dictionary
        )


def test_error_handling_invalid_file(tmp_path, field_dictionary, api_key):
    """Test error handling with corrupted Excel file."""
    invalid_file = tmp_path / "corrupted.xlsx"
    invalid_file.write_text("This is not a valid Excel file")

    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    analyzer = AnalyzerService(ai_provider=provider)

    with pytest.raises((ValueError, Exception)):
        analyzer.extract_template(
            file_path=str(invalid_file), field_dict=field_dictionary
        )


def test_error_handling_missing_api_key():
    """Test that missing API key is handled gracefully."""
    # Temporarily clear environment variables
    original_openai = os.environ.pop("OPENAI_API_KEY", None)
    original_anthropic = os.environ.pop("ANTHROPIC_API_KEY", None)

    try:
        with pytest.raises((ValueError, Exception)):
            AnalyzerService(ai_provider="openai")
    finally:
        # Restore environment variables
        if original_openai:
            os.environ["OPENAI_API_KEY"] = original_openai
        if original_anthropic:
            os.environ["ANTHROPIC_API_KEY"] = original_anthropic
