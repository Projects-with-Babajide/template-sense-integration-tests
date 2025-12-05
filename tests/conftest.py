"""Shared pytest configuration and fixtures."""

import os
import pytest
from dotenv import load_dotenv


def pytest_configure(config):
    """Load environment variables before running tests."""
    load_dotenv()


@pytest.fixture(scope="session")
def validate_environment():
    """Validate required environment variables are set."""
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))

    if not (has_openai or has_anthropic):
        pytest.exit(
            "ERROR: No AI provider API key found. "
            "Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file"
        )
