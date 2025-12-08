"""Wrapper around Template Sense AnalyzerService with safe defaults."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from app.constants import (
    DEFAULT_FIELD_DICTIONARY,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    DEFAULT_LOG_LEVEL,
    ENV_LOG_LEVEL,
    ENV_MODEL,
    ENV_PROVIDER,
)
from template_sense.ai_providers.config import AIConfig
from template_sense.analyzer import extract_template_structure
from template_sense.errors import AIProviderError


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure basic logging using environment configuration."""

    log_level = os.getenv(ENV_LOG_LEVEL, DEFAULT_LOG_LEVEL).upper()
    logging.basicConfig(level=getattr(logging, log_level, logging.INFO))


class AnalyzerService:
    """Service to analyze Excel templates via Template Sense."""

    def __init__(
        self,
        ai_provider: str | None = None,
        ai_model: str | None = None,
        field_dictionary: dict[str, list[str]] | None = None,
    ) -> None:
        self.ai_provider = (
            ai_provider or os.getenv(ENV_PROVIDER) or DEFAULT_PROVIDER
        ).lower()
        self.ai_model = ai_model or os.getenv(ENV_MODEL) or DEFAULT_MODEL
        self.field_dictionary = field_dictionary or DEFAULT_FIELD_DICTIONARY

        configure_logging()
        logger.debug(
            "Initialized AnalyzerService with provider=%s, model=%s",
            self.ai_provider,
            self.ai_model,
        )

    def _build_ai_config(self) -> AIConfig:
        provider = (os.getenv(ENV_PROVIDER) or self.ai_provider).lower()
        api_key_env = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
        api_key = os.getenv(api_key_env)

        if not api_key:
            raise AIProviderError(
                provider_name=provider,
                error_details=f"Missing required environment variable: {api_key_env}",
            )

        model = os.getenv(ENV_MODEL) or self.ai_model
        return AIConfig(provider=provider, api_key=api_key, model=model)

    def analyze(self, file_path: str | Path) -> dict[str, Any]:
        """Run the Template Sense analyzer and return extracted metadata."""

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        logger.info("Starting template analysis for %s", path)

        ai_config = self._build_ai_config()
        try:
            result = extract_template_structure(
                file_path=str(path),
                field_dictionary=self.field_dictionary,
                ai_config=ai_config,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Template analysis failed: %s", exc)
            raise

        logger.info("Template analysis completed for %s", path)
        return result
